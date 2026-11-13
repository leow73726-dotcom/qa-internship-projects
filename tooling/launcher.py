"""Start local demo applications and own their regression-test lifecycle."""
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import argparse
import os
import shutil
import socket
import subprocess
import sys
import time

import requests

ROOT=Path(__file__).resolve().parents[1]
PROJECTS={
    'swagcart-qa':(3200,'/','static'),
    'clinicflow-qa':(9966,'/petclinic/actuator/health','spring'),
    'bankflow-qa':(8087,'/parabank/','tomcat'),
}


def find_java():
    candidates=[]
    if os.getenv('JAVA_HOME'):
        candidates.append(Path(os.environ['JAVA_HOME'])/'bin/java.exe')
    candidates.extend(Path('C:/Program Files/Eclipse Adoptium').glob('jdk-21*/bin/java.exe'))
    candidates.extend(Path('C:/Program Files/Java').glob('jdk-2*/bin/java.exe'))
    system=shutil.which('java')
    if system:
        candidates.append(Path(system))
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    raise RuntimeError('Java 21+ is required for the Java demo projects.')


class SPAHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path=self.path.split('?',1)[0]
        if path.endswith('.html') and not Path(self.translate_path(path)).exists():
            self.path='/index.html'
        super().do_GET()


def app_command(name,port,kind):
    project=ROOT/name
    if kind=='static':
        return [sys.executable,str(Path(__file__).resolve()),'--static-site',str(project/'runtime/site'),'--port',str(port)]
    java=find_java()
    if kind=='spring':
        jar=project/'runtime/clinicflow.jar'
        return [java,'-jar',str(jar),'--server.address=127.0.0.1',f'--server.port={port}']
    tomcat=ROOT/'tooling/apache-tomcat-11.0.27'
    state=project/'.state/tomcat'
    state.mkdir(parents=True,exist_ok=True)
    for directory in ['conf','bin']:
        if not (state/directory).exists():
            shutil.copytree(tomcat/directory,state/directory)
    for directory in ['webapps','logs','temp','work']:
        (state/directory).mkdir(exist_ok=True)
    # App data lives in this independent local Tomcat instance.
    source=project/'runtime/parabank.war'
    target=state/'webapps/parabank.war'
    if not target.exists() or source.stat().st_mtime>target.stat().st_mtime:
        shutil.copy2(source,target)
    (state/'conf/server.xml').write_text(f'''<Server port="-1"><Service name="BankFlow"><Connector address="127.0.0.1" port="{port}" protocol="HTTP/1.1" connectionTimeout="20000"/><Engine name="Catalina" defaultHost="localhost"><Host name="localhost" appBase="webapps" unpackWARs="true" autoDeploy="true"/></Engine></Service></Server>''',encoding='utf-8')
    cp=os.pathsep.join(str(tomcat/'bin'/name) for name in ['bootstrap.jar','tomcat-juli.jar'])
    return [java,f'-Dcatalina.home={tomcat}',f'-Dcatalina.base={state}',f'-Djava.io.tmpdir={state}/temp','-classpath',cp,'org.apache.catalina.startup.Bootstrap','start']


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--project',choices=PROJECTS)
    parser.add_argument('--test',action='store_true')
    parser.add_argument('--static-site')
    parser.add_argument('--port',type=int,default=3200)
    args=parser.parse_args()
    if args.static_site:
        ThreadingHTTPServer(('127.0.0.1',args.port),partial(SPAHandler,directory=args.static_site)).serve_forever()
        return 0
    if not args.project:
        parser.error('--project is required')
    project=ROOT/args.project
    port,health,kind=PROJECTS[args.project]
    with socket.socket() as probe:
        if probe.connect_ex(('127.0.0.1',port))==0:
            raise RuntimeError(f'Port {port} is in use. Stop the manually started demo first.')
    reports=project/'reports'
    reports.mkdir(exist_ok=True)
    env=os.environ.copy()
    driver=ROOT/'tooling/drivers/chromedriver-win64/chromedriver.exe'
    if driver.exists():
        env['CHROMEDRIVER']=str(driver)
    command=app_command(args.project,port,kind)
    with (reports/'server.log').open('w',encoding='utf-8') as log:
        process=subprocess.Popen(command,cwd=project,env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        try:
            deadline=time.monotonic()+150
            while time.monotonic()<deadline:
                if process.poll() is not None:
                    raise RuntimeError('Application startup failed. Read reports/server.log.')
                try:
                    if requests.get(f'http://127.0.0.1:{port}'+health,timeout=2).status_code==200:
                        break
                except requests.RequestException:
                    pass
                time.sleep(.3)
            else:
                raise RuntimeError('Startup timed out. Read reports/server.log.')
            print(f'{args.project}: http://127.0.0.1:{port}'+('/petclinic/swagger-ui.html' if kind=='spring' else '/parabank/' if kind=='tomcat' else '/'),flush=True)
            if args.test:
                return subprocess.run([sys.executable,'-m','pytest','qa','-q','--junitxml=reports/results.xml'],cwd=project,env=env).returncode
            print('Keep this window open. Press Ctrl+C to stop.',flush=True)
            while process.poll() is None:
                time.sleep(.5)
            return process.returncode
        except KeyboardInterrupt:
            return 0
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=8)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)


if __name__=='__main__':
    raise SystemExit(main())

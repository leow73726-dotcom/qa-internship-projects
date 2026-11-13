"""Rebuild the two local demo applications through TLS-verified Maven Central downloads."""
from http.server import ThreadingHTTPServer
from pathlib import Path
import argparse
import shutil
import subprocess
import threading
import sys

from launcher import ROOT, find_java
import maven_https_bridge as bridge


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('project',choices=['clinicflow-qa','bankflow-qa'])
    parser.add_argument('--offline',action='store_true',help='Use previously cached Maven dependencies only')
    parser.add_argument('--repository',type=Path,help='Optional existing Maven dependency cache')
    args=parser.parse_args()
    project=ROOT/args.project
    state=ROOT/'.state/build'
    state.mkdir(parents=True,exist_ok=True)
    bridge.cache=state/'https-cache'
    bridge.cache.mkdir(exist_ok=True)
    maven=ROOT/'tooling/apache-maven-3.10.0'
    boot=next((maven/'boot').glob('plexus-classworlds-*.jar'))
    server=ThreadingHTTPServer(('127.0.0.1',0),bridge.Handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True)
    thread.start()
    settings=state/'settings.xml'
    settings.write_text(f'<settings><mirrors><mirror><id>qa-local-https-client</id><mirrorOf>*</mirrorOf><url>http://127.0.0.1:{server.server_port}/central/</url></mirror></mirrors></settings>',encoding='utf-8')
    repository=args.repository.resolve() if args.repository else state/'maven-cache'
    command=[find_java(),f'-Dmaven.home={maven}',f'-Dclassworlds.conf={maven}/bin/m2.conf',f'-Dmaven.multiModuleProjectDirectory={project}','-classpath',str(boot),'org.codehaus.plexus.classworlds.launcher.Launcher','-B','-f','pom.qa.xml','-s',str(settings),f'-Dmaven.repo.local={repository}','-Dmaven.test.skip=true','package']
    if args.offline:
        command.insert(-1,'-o')
    reports=project/'reports'
    reports.mkdir(exist_ok=True)
    try:
        print('Building source; first build downloads dependencies. See reports/build.log.',flush=True)
        with (reports/'build.log').open('w',encoding='utf-8') as log:
            result=subprocess.run(command,cwd=project,stdout=log,stderr=subprocess.STDOUT)
    finally:
        server.shutdown()
        server.server_close()
    if result.returncode:
        print((reports/'build.log').read_text(encoding='utf-8',errors='replace')[-6000:])
        return result.returncode
    artifact=project/('target/spring-petclinic-rest-4.0.2.jar' if args.project=='clinicflow-qa' else 'target/parabank-6.0.0-SNAPSHOT.war')
    runtime=project/'runtime'/('clinicflow.jar' if args.project=='clinicflow-qa' else 'parabank.war')
    shutil.copy2(artifact,runtime)
    print('Built and updated '+str(runtime))
    return 0


if __name__=='__main__':
    raise SystemExit(main())

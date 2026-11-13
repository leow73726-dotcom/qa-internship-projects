from pathlib import Path
import subprocess
import sys

root=Path(__file__).resolve().parents[1]
python=root/'.venv/Scripts/python.exe'
if not python.exists():
    result=subprocess.run([sys.executable,str(root/'setup.py')],cwd=root)
    if result.returncode:
        input('Setup failed. Press Enter to close.')
        raise SystemExit(result.returncode)
names=['swagcart-qa','clinicflow-qa','bankflow-qa']
print('1. 电商页面自动化  2. 诊所接口测试  3. 银行交易测试')
selected=input('选择项目 1/2/3：').strip()
if selected not in {'1','2','3'}:
    raise SystemExit('请选择 1、2 或 3。')
mode=input('输入 1 打开应用，输入 2 执行自动测试：').strip()
command=[str(python),str(root/'tooling/launcher.py'),'--project',names[int(selected)-1]]
if mode=='2':
    command.append('--test')
result=subprocess.run(command,cwd=root)
input('按回车结束。')
raise SystemExit(result.returncode)

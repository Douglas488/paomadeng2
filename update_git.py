import subprocess
import tkinter as tk
from tkinter import messagebox

def run_command(command, cwd=None):
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, text=True, capture_output=True)
        print(f"Running command: {command} in {cwd}")
        print(f"STDOUT: {result.stdout.strip()}")
        print(f"STDERR: {result.stderr.strip()}")
        if result.returncode != 0:
            raise Exception(f"Command failed with return code {result.returncode}")
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None

def show_message(title, message):
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    messagebox.showinfo(title, message)

def update_git(target_dir):
    # 确保目标目录是一个 Git 仓库
    result = run_command('git rev-parse --is-inside-work-tree', cwd=target_dir)
    if result is None or result.returncode != 0:
        show_message("错误", "当前目录不是一个 Git 仓库。请确保你在正确的目录中运行此脚本。")
        return

    # 配置 Git 用户信息
    run_command('git config user.name "Douglas488"', cwd=target_dir)
    run_command('git config user.email "sim892284946@gmail.com"', cwd=target_dir)

    # 添加更改到暂存区
    result = run_command('git add data.txt', cwd=target_dir)
    if result is None:
        show_message("失败", "无法将更改添加到暂存区。")
        return

    # 提交更改
    commit_message = "Update data.txt content"
    result = run_command(f'git commit -m "{commit_message}"', cwd=target_dir)
    if result is None or result.returncode != 0:
        show_message("失败", "提交更改失败。确保有更改可以提交。")
        return

    # 推送更改到远程仓库
    result = run_command('git push origin main', cwd=target_dir)
    if result is None or result.returncode != 0:
        show_message("上传失败", "推送更改失败。")
        return

    # 成功消息
    show_message("上传成功", "修改成功! 数据已成功更新并推送。")

if __name__ == "__main__":
    target_dir = r"C:\Users\Administrator\Desktop\paomadeng2"  # 修改为你的目标目录
    update_git(target_dir)

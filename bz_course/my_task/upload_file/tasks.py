from my_task.main import app
@app.task(name="upload")
def upload():
    print('上传文件成功')
    return 'file'
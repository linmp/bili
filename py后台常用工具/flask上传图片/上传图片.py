# 上传照片test接口
@app.route("/uploadpic", methods=["GET", "POST"])
def uploadpic():
    img = request.files.get('pic')
    path = basedir + "/static/photo/"

    # img.filename = datetime.now().strftime("%Y%m%d%H%M%S") + img.filename
    file_path = path + img.filename
    img.save(file_path)
    # pathfile = "/static/photo/" + img.filename
    data = {"msg": "success"}
    payload = json.dumps(data)
    return payload, 200
    # return pathfile,200

from app import create_app

app = create_app("develop")  # 工厂函数模式选择

if __name__ == '__main__':
    app.run()

def init_db():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()

from flask import Flask
from views import scanHash
from views import scanBuffer

app = Flask(__name__)
app.register_blueprint(scanHash.scan_hash)
app.register_blueprint(scanBuffer.scan_buffer)
def main():
    app=Flask(__name__)

    app.run()

if __name__=='__main__':
    main()
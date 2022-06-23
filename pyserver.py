# Python 3 server example
import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from pymongo import MongoClient

hostName = "localhost"
serverPort = 8080

client = MongoClient("mongodb+srv://test:test@cluster0.anx9a.mongodb.net/?retryWrites=true&w=majority")
db = client.pasta
collection = db.pastas

class MyServer(BaseHTTPRequestHandler):

    # def read_html_template(path):
    #     """function to read HTML file"""
    #     try:
    #         with open(path) as f:
    #             file = f.read()
    #     except Exception as e:
    #         file = e
    #     return file
    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("h", "yo")
        self.end_headers()

        path = self.path

        if path == '/':
            # with open('home.html', 'rb') as content:
            #     self.wfile.write(content.read())
                # self.wfile.write(bytes(file, "utf-8"))
                

            
            self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
            # self.wfile.write(bytes("<p>%s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<form method='POST' enctype='multipart/form-data' action='/'>", "utf-8"))
            self.wfile.write(bytes("<div><textarea rows='4' cols='50' name='pasta' id='pasta' placeholder='pasta goes here'></textarea></div>", "utf-8"))
            self.wfile.write(bytes("<div><button>Send!</button></div>", "utf-8"))
            # self.wfile.write(bytes("", "utf-8"))
            # self.wfile.write(bytes("", "utf-8"))
            self.wfile.write(bytes("</form>", "utf-8"))
            self.wfile.write(bytes("</body>", "utf-8"))

            
            cursor = collection.find().sort("_id", -1).limit(10)
            for document in cursor:
                self.wfile.write(bytes("<h3>%s</h3>" % document['body'], "utf-8"))


        # self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        # self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        # self.wfile.write(bytes("<body>", "utf-8"))
        # self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        # self.wfile.write(bytes("</body></html>", "utf-8"))

    def do_POST(self):
        path = self.path

        if path == '/':
            print("ok")
            c_type, p_dict = cgi.parse_header(self.headers.get('Content-Type'))
            p_dict['boundary'] = bytes(p_dict['boundary'], "utf-8")
            content_len = int(self.headers.get('Content-length'))
            p_dict['CONTENT-LENGTH'] = content_len
            if c_type =="multipart/form-data":
                fields = cgi.parse_multipart(self.rfile, p_dict)
                new_pasta = fields.get("pasta")[0]


                mydict = { "name": "user1", "body": new_pasta }
                collection.insert_one(mydict)

                print(new_pasta)
                print("ok")
                print(self.headers.get('h'))

            self.send_response(301)
            self.send_header('Location','/')
            self.end_headers()

            # ctype,pdict = cgi.parse_header(self.headers.get('Content-type'))
            # pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            # if ctype == 'multipart/form-data':
            #     query = cgi.parse_multipart(self.rfile, pdict)
            # self.send_response(301)
            # self.end_headers()
            # self.wfile.write('Post!')

            # else:
            #     print("not ok")

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
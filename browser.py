import webbrowser

f = open("helloworld.html", "w")

message = """<html>
<head>
<title>Flag-dle</title>
<style> img {
  border: 5px solid #555;
  width: 49%;
}
</style>
</head>
<body><img src="flag.png" alt="whataflag"><img src="flag_uncolored.png" alt="b&w">
<p>Can you guess what flag it is?</p></body>
</html>"""

f.write(message)
f.close()

webbrowser.open_new_tab("helloworld.html")

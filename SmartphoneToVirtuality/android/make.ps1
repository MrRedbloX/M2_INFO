javac -cp .\lib\java-json.jar .\Server.java -d .\class\
cd .\class\
jar -cvfm ../Server.jar MANIFEST.MF *.class
cd ..
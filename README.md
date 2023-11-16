msh:穆宇浩，索凯龙，黄鹏瑀；基于电影信息知识图谱的知识问答系统  
KG-movie.pdf is the document of our project  
our project is divided into four steps  
relation_database->ontology->graph_database->reasoning  
to run our project,you should follow these steps  
1.first ensure your computer has the java environment  
2.download the three parts of jena and decompression them.  
3.configure the environment variables of jena,the first named "JENA_HOME"(don't copy the double quotation mark),and the value is the path of the folder named "apache-jena-3.5.0",and the other named "FUSEKI_HOME" and the value is the  path of the folder named "apache-jena-fuseki-3.5.0"  
4.modify the file in  "apache-jena-fuseki-3.5.0\run\configuration\fuseki_conf.ttl",in line 27,36,44,to make sure the path of rules.ttl,ontology.ttl and tdb is true.  
5.open the terminal in "apache-jena-fuseki-3.5.0" and execute the command".\fuseki-server.bat"  
then you open the jena server,one way to use it is through python the project in "kg_movie" is an example of use it to query.  

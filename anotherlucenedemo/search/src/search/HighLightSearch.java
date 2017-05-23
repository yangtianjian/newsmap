package search;

import java.io.File;
import java.io.FileReader;
import java.nio.file.FileSystems;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

class Index {
    // 建立索引
    public void index() {
        IndexWriter indexWriter = null;

        try {
            // 1、创建Directory
            //JDK 1.7以后 open只能接收Path
            Directory directory = FSDirectory.open(FileSystems.getDefault().getPath("F:/search/index"));
            // 2、创建IndexWriter
            Analyzer analyzer = new StandardAnalyzer();
            IndexWriterConfig indexWriterConfig = new IndexWriterConfig(analyzer);
            indexWriter = new IndexWriter(directory, indexWriterConfig);
            indexWriter.deleteAll();//清除以前的index
            //要搜索的File路径
            File dFile = new File("F:/search/data");
            File[] files = dFile.listFiles();
            for (File file : files) {
                // 3、创建Document对象
                Document document = new Document();
                // 4、为Document添加Field
                // 第三个参数是FieldType 但是定义在TextField中作为静态变量，看API也不好知道怎么写
                document.add(new Field("content", new FileReader(file), TextField.TYPE_NOT_STORED));
                document.add(new Field("filename", file.getName(), TextField.TYPE_STORED));
                document.add(new Field("filepath", file.getAbsolutePath(), TextField.TYPE_STORED));

                // 5、通过IndexWriter添加文档到索引中
                indexWriter.addDocument(document);
            }

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (indexWriter != null) {
                    indexWriter.close();
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}

/*
 *  创建Directory
    创建IndexReader    
    根据IndexReader创建IndexSearch        
    创建搜索的Query 
    根据searcher搜索并且返回TopDocs  
    根据TopDocs获取ScoreDoc对象        
    根据searcher和ScoreDoc对象获取具体的Document对象          
    根据Document对象获取需要的值
 * 
 */

class Search {  
    /** 
     * 搜索 
     */  
    public void search(String keyWord) {  
        DirectoryReader directoryReader = null;  
        try {  
            // 1、创建Directory  
            Directory directory = FSDirectory.open(FileSystems.getDefault().getPath("F:/search/index"));
            // 2、创建IndexReader  
            directoryReader = DirectoryReader.open(directory);  
            // 3、根据IndexReader创建IndexSearch  
            IndexSearcher indexSearcher = new IndexSearcher(directoryReader);  

            // 4、创建搜索的Query  
            Analyzer analyzer = new StandardAnalyzer();  
            // 创建parser来确定要搜索文件的内容，第一个参数为搜索的域  
            QueryParser queryParser = new QueryParser("content", analyzer);  
            // 创建Query表示搜索域为content包含UIMA的文档  
            Query query = queryParser.parse(keyWord);  

            // 5、根据searcher搜索并且返回TopDocs  
            TopDocs topDocs = indexSearcher.search(query, 10);  
            System.out.println("查找到的文档总共有："+topDocs.totalHits);

            // 6、根据TopDocs获取ScoreDoc对象  
            ScoreDoc[] scoreDocs = topDocs.scoreDocs;  
            for (ScoreDoc scoreDoc : scoreDocs) {  

                // 7、根据searcher和ScoreDoc对象获取具体的Document对象  
                Document document = indexSearcher.doc(scoreDoc.doc);  

                // 8、根据Document对象获取需要的值  
                System.out.println(document.get("filename") + " " + document.get("filepath"));  
            }  

        } catch (Exception e) {  
            e.printStackTrace();  
        } finally {  
            try {  
                if (directoryReader != null) {  
                    directoryReader.close();  
                }  
            } catch (Exception e) {  
                e.printStackTrace();  
            }  
        }  
    }  
}  

public class HighLightSearch {
    public static void main(String args[]) {
        Index newIndex = new Index();
        newIndex.index();
        Search newSearch = new Search();
        newSearch.search("猫咪");
    }
}
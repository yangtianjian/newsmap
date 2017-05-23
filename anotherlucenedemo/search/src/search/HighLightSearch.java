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
    // ��������
    public void index() {
        IndexWriter indexWriter = null;

        try {
            // 1������Directory
            //JDK 1.7�Ժ� openֻ�ܽ���Path
            Directory directory = FSDirectory.open(FileSystems.getDefault().getPath("F:/search/index"));
            // 2������IndexWriter
            Analyzer analyzer = new StandardAnalyzer();
            IndexWriterConfig indexWriterConfig = new IndexWriterConfig(analyzer);
            indexWriter = new IndexWriter(directory, indexWriterConfig);
            indexWriter.deleteAll();//�����ǰ��index
            //Ҫ������File·��
            File dFile = new File("F:/search/data");
            File[] files = dFile.listFiles();
            for (File file : files) {
                // 3������Document����
                Document document = new Document();
                // 4��ΪDocument���Field
                // ������������FieldType ���Ƕ�����TextField����Ϊ��̬��������APIҲ����֪����ôд
                document.add(new Field("content", new FileReader(file), TextField.TYPE_NOT_STORED));
                document.add(new Field("filename", file.getName(), TextField.TYPE_STORED));
                document.add(new Field("filepath", file.getAbsolutePath(), TextField.TYPE_STORED));

                // 5��ͨ��IndexWriter����ĵ���������
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
 *  ����Directory
    ����IndexReader    
    ����IndexReader����IndexSearch        
    ����������Query 
    ����searcher�������ҷ���TopDocs  
    ����TopDocs��ȡScoreDoc����        
    ����searcher��ScoreDoc�����ȡ�����Document����          
    ����Document�����ȡ��Ҫ��ֵ
 * 
 */

class Search {  
    /** 
     * ���� 
     */  
    public void search(String keyWord) {  
        DirectoryReader directoryReader = null;  
        try {  
            // 1������Directory  
            Directory directory = FSDirectory.open(FileSystems.getDefault().getPath("F:/search/index"));
            // 2������IndexReader  
            directoryReader = DirectoryReader.open(directory);  
            // 3������IndexReader����IndexSearch  
            IndexSearcher indexSearcher = new IndexSearcher(directoryReader);  

            // 4������������Query  
            Analyzer analyzer = new StandardAnalyzer();  
            // ����parser��ȷ��Ҫ�����ļ������ݣ���һ������Ϊ��������  
            QueryParser queryParser = new QueryParser("content", analyzer);  
            // ����Query��ʾ������Ϊcontent����UIMA���ĵ�  
            Query query = queryParser.parse(keyWord);  

            // 5������searcher�������ҷ���TopDocs  
            TopDocs topDocs = indexSearcher.search(query, 10);  
            System.out.println("���ҵ����ĵ��ܹ��У�"+topDocs.totalHits);

            // 6������TopDocs��ȡScoreDoc����  
            ScoreDoc[] scoreDocs = topDocs.scoreDocs;  
            for (ScoreDoc scoreDoc : scoreDocs) {  

                // 7������searcher��ScoreDoc�����ȡ�����Document����  
                Document document = indexSearcher.doc(scoreDoc.doc);  

                // 8������Document�����ȡ��Ҫ��ֵ  
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
        newSearch.search("è��");
    }
}
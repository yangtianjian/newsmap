/**
 * <p>Title: </p>
 *
 * <p>Description: </p>
 *
 * <p>Copyright: Copyright (c) 2009</p>
 *
 * <p>Company: </p>
 *
 * @author not attributable
 * @version 1.0
 */
package lucence;
import org.apache.lucene.*;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.analysis.*;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.*;
import org.apache.lucene.store.*;
import java.io.*;
import org.apache.lucene.search.*;
import org.apache.lucene.queryParser.*;
import java.util.*;
import org.apache.lucene.util.Version;
import org.apache.lucene.index.*;
import javax.swing.*;
public class LuceneProc {
    public LuceneProc() {
    }
    public static final int MaxHits = 100;
    public static int CreateIndex(String srcpath,String indexpath) {
        IndexWriter writer;
        File docDir = new File(srcpath);
        if (!docDir.exists() || !docDir.canRead()) {
        	//System.out.println("建立索引出错，文档路径不存在或不可读。");
            return 1;//文档路径不存在或不可读。
        }
        File indexDir = new File(indexpath);
        if(indexDir.exists()){
            delete(indexDir);
        }
        try {
            writer = new IndexWriter(FSDirectory.open(indexDir), new StandardAnalyzer(Version.LUCENE_CURRENT),
                                     true, IndexWriter.MaxFieldLength.LIMITED);
            IndexFiles.indexDocs(writer, docDir);
            writer.optimize();
            writer.close();
        } catch (Exception ex) {
        	//System.out.println("建立索引出错，索引过程出现异常。");
            return 2;//there is a exception when index the file.
        }
        System.out.println("建立索引完成。");
        return 0;//create index successfully.
    }
    public static int SearchProc(String indexpath,String queryString,ArrayList alist){
        try {
            IndexReader reader = IndexReader.open(FSDirectory.open(new File(indexpath)), true);
            IndexSearcher searcher = new IndexSearcher(reader);
            Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_CURRENT);
            QueryParser qp = new QueryParser(Version.LUCENE_CURRENT,"contents", analyzer);
            Query query = qp.parse(queryString);
            TopDocs hits = searcher.search(query,MaxHits);
            System.out.println("查询"+queryString+"成功，结果为"+hits.totalHits+"条。");
            //System.out.println(hits.totalHits);
            for (int i=0; i<hits.totalHits; i++) {
                Document doc = searcher.doc(hits.scoreDocs[i].doc);
                String[] ls = new String[2];
                ls[0]=doc.get("path");
                ls[1]=""+hits.scoreDocs[i].score;
                alist.add(ls);
                System.out.println("第" + i + "条：" + doc.get("path"));
            }
        } catch (IOException ex) {
            System.out.println("Create searcher failed!");
            return 1;
        }
        catch (ParseException ex1) {
            System.out.println("parse error!");
            return 2;
        }
        return 0;
    }
    public static void delete(File f){
        if(f.isDirectory()){
            File[] files = f.listFiles();
            for(int i=0;i<files.length;i++)
            {
               if( files[i].isDirectory()){
                   delete(files[i]);
               }else{
                   files[i].delete();
               }
            }
            f.delete();
        }
        else f.delete();
    }
//    public static void main(String args[]){
//        if(CreateIndex("C:\\Documents and Settings\\Administrator\\桌面\\我","C:\\index\\")==1){
//            System.out.println("Create index successful!");
//            ArrayList alist = new ArrayList();
//            SearchProc("C:\\index\\","error",alist);
//        }
//        else{
//            System.out.println("Create index failed!");
//        }
//    }
}

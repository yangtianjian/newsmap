package net.paoding.analysis.t;

import net.paoding.analysis.analyzer.PaodingAnalyzer;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field.Store;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.RAMDirectory;
import org.junit.Assert;

public class InMemoryShortExample {

    private static final Analyzer ANALYZER = new PaodingAnalyzer();

    public static void main(String[] args) {
        // Construct a RAMDirectory to hold the in-memory representation
        // of the index.

        try {
//            Directory idx = FSDirectory.open(new File("F:/data/lucene/fix"));
            Directory idx = new RAMDirectory();
            // Make an writer to create the index
            IndexWriterConfig iwc = new IndexWriterConfig(ANALYZER);

            IndexWriter writer = new IndexWriter(idx, iwc);

            // Add some Document objects containing quotes
            writer.addDocument(createDocument("维基百科:关于中文维基百科", "维基百科:关于中文维基百科"));
            writer.addDocument(createDocument("三维基础百科", "维基百科:关于中文维基百科"));
            writer.addDocument(createDocument("我们的世界", "维基百科:关于中文维基百科"));
            writer.addDocument(createDocument("平凡的世界", "维基百科:关于中文维基百科"));

            writer.commit();

            IndexSearcher searcher = new IndexSearcher(DirectoryReader.open(idx));
            TopDocs topDocs = searcher.search(new QueryParser("title", ANALYZER).parse("title:'维基'"), 10);
            Assert.assertTrue(topDocs.totalHits > 0);
            System.out.printf("totalHits:%d%n", topDocs.totalHits);
            ScoreDoc[] scoreDocs = topDocs.scoreDocs;
            for (ScoreDoc scoreDoc : scoreDocs) {
                System.out.println(scoreDoc.toString());
                System.out.println(searcher.doc(scoreDoc.doc));
            }
        } catch (Exception ioe) {
            // In this example we aren't really doing an I/O, so this
            // exception should never actually be thrown.
            ioe.printStackTrace();
        }
    }

    /**
     * Make a Document object with an un-indexed title field and an indexed
     * content field.
     */
    private static Document createDocument(String title, String content) {
        Document doc = new Document();

        // Add the title as an unindexed field...
        doc.add(new TextField("title", title, Store.YES));

        // ...and the content as an indexed field. Note that indexed
        // Text fields are constructed using a Reader. Lucene can read
        // and index very large chunks of text, without storing the
        // entire content verbatim in the index. In this example we
        // can just wrap the content string in a StringReader.
        doc.add(new TextField("content", content, Store.YES));

        return doc;
    }
}

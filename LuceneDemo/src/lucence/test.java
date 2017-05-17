package lucence;

import java.util.ArrayList;

public class test {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		ArrayList reslist = new ArrayList();
		reslist.clear();
		String docpath="C:/Users/Desktop/第四季度";
		String indexpath="C:/Users/Desktop/index";
        int i=LuceneProc.CreateIndex(docpath, indexpath);
        if(i!=0) {System.out.println("建立索引失败！");}
        else{
        	LuceneProc.SearchProc(indexpath, "装置", reslist);
        }
        
	}

}

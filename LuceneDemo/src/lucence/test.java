package lucence;

import java.util.ArrayList;

public class test {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		ArrayList reslist = new ArrayList();
		reslist.clear();
		String docpath="C:/Users/Desktop/���ļ���";
		String indexpath="C:/Users/Desktop/index";
        int i=LuceneProc.CreateIndex(docpath, indexpath);
        if(i!=0) {System.out.println("��������ʧ�ܣ�");}
        else{
        	LuceneProc.SearchProc(indexpath, "װ��", reslist);
        }
        
	}

}

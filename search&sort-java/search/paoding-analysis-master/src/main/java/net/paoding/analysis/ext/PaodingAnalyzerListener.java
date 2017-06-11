/**
 * 
 */
package net.paoding.analysis.ext;

import java.util.Collection;

import net.paoding.analysis.dictionary.Word;

/**
 * @author ZhenQin
 *
 */
public interface PaodingAnalyzerListener {

	void readDic(String dicPath);
	
	
	void readDicFinished(String dicPath, Collection<Word> conllec);
	
	
	void refreshDic(String dicPath, Collection<Word> conllec);
	
	void readCompileDic(String dicPath);
	
	void readCompileDicFinished(String dicPath, Collection<Word> conllec);

}

/**
 * Copyright 2007 The Apache Software Foundation
 * <p>
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * <p>
 * http://www.apache.org/licenses/LICENSE-2.0
 * <p>
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package net.paoding.analysis.analyzer.impl;

import net.paoding.analysis.analyzer.TokenCollector;
import org.apache.lucene.analysis.tokenattributes.PackedTokenAttributeImpl;

import java.util.Iterator;
import java.util.LinkedList;


/**
 * @author Zhiliang Wang [qieqie.wang@gmail.com]
 * @since 1.1
 */
public class MaxWordLengthTokenCollector implements TokenCollector {

    /**
     * 存储当前被knife分解而成的Token对象
     */
    private LinkedList<PackedTokenAttributeImpl> tokens = new LinkedList<PackedTokenAttributeImpl>();

    private PackedTokenAttributeImpl candidate;

    private PackedTokenAttributeImpl last;


    public MaxWordLengthTokenCollector() {
    }

    public Iterator<PackedTokenAttributeImpl> iterator() {
        if (candidate != null) {
            this.tokens.add(candidate);
            candidate = null;
        }
        Iterator<PackedTokenAttributeImpl> iter = this.tokens.iterator();
        this.tokens = new LinkedList<PackedTokenAttributeImpl>();
        return iter;
    }

    public void collect(String word, int offset, int end) {
        PackedTokenAttributeImpl c = candidate != null ? candidate : last;
        if (c == null) {
            candidate = new PackedTokenAttributeImpl();
            candidate.append(word);
            candidate.setOffset(offset, end);
        } else if (offset == c.startOffset()) {
            if (end > c.endOffset()) {
                candidate = new PackedTokenAttributeImpl();
                candidate.append(word);
                candidate.setOffset(offset, end);
            }
        } else if (offset > c.startOffset()) {
            if (candidate != null) {
                select(candidate);
            }
            if (end > c.endOffset()) {
                candidate = new PackedTokenAttributeImpl();
                candidate.append(word);
                candidate.setOffset(offset, end);
            } else {
                candidate = null;
            }
        } else if (end >= c.endOffset()) {
            if (last != null && last.startOffset() >= offset
                    && last.endOffset() <= end) {
                for (Iterator<PackedTokenAttributeImpl> iter = tokens.iterator(); iter.hasNext(); ) {
                    last = iter.next();
                    if (last.startOffset() >= offset && last.endOffset() <= end) {
                        iter.remove();
                    }
                }
            }
            last = null;
            candidate = new PackedTokenAttributeImpl();
            candidate.append(word);
            candidate.setOffset(offset, end);
        }
    }

    protected void select(PackedTokenAttributeImpl t) {
        this.tokens.add(t);
        this.last = t;
    }

}

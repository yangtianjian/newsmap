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
package net.paoding.analysis.analyzer;

import net.paoding.analysis.knife.Collector;
import org.apache.lucene.analysis.tokenattributes.PackedTokenAttributeImpl;

import java.util.Iterator;

/**
 *
 * @author Zhiliang Wang [qieqie.wang@gmail.com]
 *
 * @since 1.1
 */
public interface TokenCollector extends Collector {

    /**
     *
     * @return
     */
    Iterator<PackedTokenAttributeImpl> iterator();
}

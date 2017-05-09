#ifndef __LRU_CACHE_H__
#define __LRU_CACHE_H__

/*
 *
 * Copyright (c) 2002 Rutgers University and Eduardo Pinheiro
 * All rights reserved.
 *
 * Permission to use, copy, modify, and distribute this software and its
 * documentation for any purpose, without fee, and without written agreement is
 * hereby granted, provided that the following conditions are met:
 *
 *    1. Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *
 *    2. Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *
 *    3. All advertising materials mentioning features or use of this
 *       software must display the following acknowledgment:
 *           This product includes software developed by
 *           Rutgers University and its contributors.
 *
 *    4. Neither the name of the University nor the names of its
 *       contributors may be used to endorse or promote products derived from
 *       this software without specific prior written permission.
 *
 * IN NO EVENT SHALL RUTGERS UNIVERSITY BE LIABLE TO ANY PARTY FOR DIRECT,
 * INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT
 * OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF RUTGERS
 * UNIVERSITY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * RUTGERS UNIVERSITY SPECIFICALLY DISCLAIMS ANY WARRANTIES,
 * INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
 * AND FITNESS FOR A PARTICULAR PURPOSE.  THE SOFTWARE PROVIDED HEREUNDER IS
 * ON AN "AS IS" BASIS, AND RUTGERS UNIVERSITY HAS NO OBLIGATION TO
 * PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
 *
 * Author:        Eduardo Pinheiro
 * Version:       1.45
 * Creation Date: 02/02/2002
 * Filename:      lrucache.H
 * History:
 *
 */

/* To use: make your objects inherit class LRUCacheEntry. Override the
   evict and tryEvict methods to do the appropriate things, ie,
   tryEvict will most likely return true always and evict will usually
   'delete' itself (the 'this' pointer), unless you know there is
   another reference to it somewhere else in memory.

   class foo : public LRUCacheEntry<int>
   {
      int the_value;

      virtual bool tryEvict () { return true; }
      virtual void evict() { delete this; ]
   };

   ...
   
   LRUCache *lru = new LRUCache<int>;
   foo *entry = new foo;
   int an_int = 32;
   foo->the_value = an_int; 
   ...

   lru->add(an_int, "a string or NULL", foo);

   foo = lru->getAndTouch(an_int);

   ...
   
*/   


#include <list>
#include <hash_map>

/*
   This file combines a generic 32-bit key identifier with a string
   (char*) identifier for an LRU cache. One can get/add/touch elements
   by using the numerical key or the string key. Useful for keeping file
   names and file handlers together.  */


struct long_eqstr
{
    bool operator()(const unsigned long s1, const unsigned long s2) const
    {
	return s1 == s2;
    }
};

/*
struct u_long_long_eqstr
{
    bool operator()(const unsigned long long s1, const unsigned long long s2) const
    {
	return s1 == s2;
    }
};
*/
/*
struct const_char_eqstr
{
    bool operator()(const char* s1, const char* s2) const
    {
	return strcmp(s1, s2) == 0;
    }
};    
*/

struct char_eqstr
{
    bool operator()(const char* s1, const char* s2) const
    {
	return strcmp(s1, s2) == 0;
    }
};    


struct eqstr
{
    bool operator()(const unsigned int s1, const unsigned int s2) const
    {
	return (s1==s2);
    }
};


template <class key>
class LRUCacheEntry
{
  public:
    key dKey;
    char *name;
    list<LRUCacheEntry *>::iterator pos;
    
    virtual bool tryEvict () = 0;
    virtual void evict () = 0;    
};


template<class key>
class LRUCache
{
    struct eqstr
    {
	bool operator()(const unsigned int s1, const unsigned int s2) const
	{
	    return (s1==s2);
	}
    };
/*
    class basicObj
    {
      public:
	obj dObj;
//	CacheObject<key> *dObj;
	key dKey;
	char *name;
	list<basicObj*>::iterator pos;
    };
*/    
    
  public:
    typedef hash_map<key, LRUCacheEntry<key>*, hash<key>, eqstr> cachemap_t;
    typedef hash_map<char*, LRUCacheEntry<key>*, hash<char*>, char_eqstr> namemap_t;
    typedef list<LRUCacheEntry<key>*> list_t;
    
  private:
    bool moved;
    list_t list;
    cachemap_t cachemap;
    namemap_t namemap;
    int size;
    int max_size;
    list_t::reverse_iterator curr;

    /* LRUCacheEntry<key> **/
    void evict ()
    {
	LRUCacheEntry<key> *nObj;
	list_t::iterator last = list.begin();
	cachemap_t::iterator it;
	namemap_t::iterator itname;
	int itCount = 0;

	while (1)
	{
            // Can't free any object. Can't allocate more! Out of mem
	    if (last==list.end())
	    {
		/* Sleep in the hopes that the algorithm thread will have allowed us to free
		   some resources */
		last = list.begin();
		itCount++;
		NOMEM(itCount>3);
		fprintf(stderr,"lrucache: sleeping before trying to free up more handlers\n");
		usleep(10000*itCount); /* Sleep 10-20 ms */
	    }
	    // this whole 'if' was only: NOMEM(last==list.end()); 
	    
	    nObj = *last;
	    INCONSISTENCY(!nObj);	    
	    it = cachemap.find(nObj->dKey);
	    INCONSISTENCY(it == cachemap.end());
	    if (nObj->name)
	    {
		itname = namemap.find(nObj->name);
		INCONSISTENCY(itname == namemap.end());
	    }
	    INCONSISTENCY(it->second != itname->second); // Sanity test
	    
	    // The object should know that it's being evicted.	
	    if (nObj->tryEvict())
		break;		
	    else
		last++;
	}

	if (nObj->name)
	    namemap.erase(itname);
	cachemap.erase(it);
	list.erase(last);
	
	/* Inform object that it is no longer reachable from this
	   cache. It should delete itself or make sure someone
	   else has a pointer to it. */
	nObj->evict(); 
//	delete (nObj->dObj); // Delete the user-supplied object.	
	size--;
//	return nObj;
    }
    
  public:
    
    LRUCache (int maxSize)
    {
	size      = 0;
	max_size  = maxSize;
	curr      = list.rend();
	moved     = false;
    }

    // Assumes it is NOT in the cache, otherwise results could be unpredictable
    void add (key dKey, char *name, LRUCacheEntry<key> * dObj)
    {
	LRUCacheEntry<key> *nObj;

	if (size==max_size)
	    evict();

	nObj = dObj;
	
	INCONSISTENCY(!nObj);
	INCONSISTENCY(isInCache(dKey));
	INCONSISTENCY(name && isInCache(name));
	
	nObj->dKey = dKey;
	nObj->name = name;
	list.push_back(nObj);
	nObj->pos  = list.end();
	nObj->pos--;
	cachemap[dKey] = nObj;
	if (name)
	    namemap[name]  = nObj;
	size++;
    }

    void remove (key dKey)
    {
	cachemap_t::iterator it;
	namemap_t::iterator itname;
	LRUCacheEntry<key> *nObj;
	
	it=cachemap.find(dKey);
	if (it == cachemap.end())
	    return;	
	cachemap.erase(it);
	nObj = it->second;
	INCONSISTENCY(!nObj);
	if (*(nObj->pos) == *curr)
	{
	    curr++;
	    moved = true;
	}
	list.erase(nObj->pos);
	if (nObj->name)
	{
	    itname = namemap.find(nObj->name);
	    INCONSISTENCY(itname == namemap.end()); // Name not found but dKey found???	    
	    namemap.erase(itname);
	}
	size--;
	INCONSISTENCY(size<0);	    
    }

    void remove (char *name)
    {
	namemap_t::iterator it;
	cachemap_t::iterator itcache;
	LRUCacheEntry<key> *nObj;
	
	it=namemap.find(name);
	if (it == namemap.end())
	    return;	
	namemap.erase(it);
	nObj = it->second;
	INCONSISTENCY(!nObj);
	if (*(nObj->pos) == *curr)
	{
	    curr++;
	    moved = true;
	}
	list.erase(nObj->pos);
	itcache = cachemap.find(nObj->dKey);
	INCONSISTENCY(itcache == cachemap.end()); // Name found but dKey not found???
	    
	cachemap.erase(itcache);
	size--;
	INCONSISTENCY(size<0);	    
    }
    
    LRUCacheEntry<key> * get (key dKey)
    {
	cachemap_t::const_iterator it;
	
	it = cachemap.find(dKey);
	if (it == cachemap.end())
	    return NULL;

	return it->second;
    }

    LRUCacheEntry<key> * get (char *name)
    {
	namemap_t::const_iterator it;
	
	it = namemap.find(name);
	if (it == namemap.end())
	    return NULL;

	return  it->second;
    }
    
    void touch (key dKey)
    {
	getAndTouch(dKey);
    }

    void touch (char *name)
    {
	getAndTouch(name);
    }

    void touch (LRUCacheEntry<key> *obj)
    {
	list.erase(obj->pos);
	list.push_back(obj);
	obj->pos = list.end();
	obj->pos--;	
    }
    
    int getSize ()
    {
	return size;
    }
    
    bool isInCache (key dKey)
    {
	return (get(dKey)!=NULL);
    }

    bool isInCache (char *name)
    {
	return (get(name)!=NULL);
    }

    LRUCacheEntry<key> * getAndTouch (key dKey)
    {
	cachemap_t::const_iterator it;
	LRUCacheEntry<key> *nObj;
	
	it = cachemap.find(dKey);
	if (it == cachemap.end())
	    return NULL;

	nObj = it->second;
	INCONSISTENCY(!nObj);
	INCONSISTENCY(nObj->dKey != dKey);
	
	if ((curr!=list.rend()) && (*(nObj->pos) == *curr))
	{
	    curr++;
	    moved = true;
	}
	
	list.erase(nObj->pos);
	list.push_back(nObj);
	nObj->pos = list.end();
	nObj->pos--;
	return nObj;
    }

    LRUCacheEntry<key> * getAndTouch (char *name)
    {
	namemap_t::const_iterator it;
	LRUCacheEntry<key> *nObj;
	
	it = namemap.find(name);
	if (it == namemap.end())
	    return NULL;
	
	nObj = it->second;
	INCONSISTENCY(!nObj);
	INCONSISTENCY(strcmp(nObj->name, name)!=0);

	if ((curr!=list.rend()) && (*(nObj->pos) == *curr))
	{
	    curr++;
	    moved = true;
	}
	
	list.erase(nObj->pos);
	list.push_back(nObj);
	nObj->pos = list.end();
	nObj->pos--;
	return nObj;
    }

    void touchCurrent ()
    {
	 LRUCacheEntry<key> *nObj;
	list_t::reverse_iterator it;

	if (curr==list.rbegin()) // Nothing to be done!
	    return;
	
	if (moved)
	    return;
	
	INCONSISTENCY(curr==list.rend());
	nObj = *curr;
	INCONSISTENCY(!nObj);
	
	it = curr;
	it++;
	
	list.erase(nObj->pos);
	list.push_back(nObj);
	nObj->pos = list.end();
	nObj->pos--;

	curr = it;
	moved = true;
    }

    LRUCacheEntry<key> * getFirst ()
    {
	LRUCacheEntry<key> *nObj;
	if (list.empty())
	    return NULL;
	curr = list.rbegin();
	moved = false;
	nObj = *curr;
	return nObj;
    }

    LRUCacheEntry<key> * getNext ()
    {
	LRUCacheEntry<key> *nObj;
	if (curr==list.rend())
	    return NULL;
	if (!moved)	    
	    curr++;
	if (curr==list.rend())
	    return NULL;	
	nObj = *curr;
	INCONSISTENCY(!nObj);
	return nObj;
    }
    
};


#endif


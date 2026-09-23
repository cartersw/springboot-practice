package dev.practice.assessment02.cache;
import org.springframework.stereotype.Component;
@Component public class SearchCacheInvalidator {
 private final KeyValueStore store;public SearchCacheInvalidator(KeyValueStore s){store=s;}
 public void invalidate(){for(String key:store.keys())if(key.startsWith("products:search:v1:"))store.delete(key);}
}

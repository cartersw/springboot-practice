package dev.practice.assessment02.service;
import java.time.Duration;
import org.springframework.stereotype.Service;import com.fasterxml.jackson.databind.ObjectMapper;
import dev.practice.assessment02.search.*;import dev.practice.assessment02.dto.*;import dev.practice.assessment02.cache.*;import dev.practice.assessment02.observation.ProductQueryGateway;
@Service public class ProductSearchService {
 private final KeyValueStore cache;private final SearchKeyFactory keys;private final ProductQueryGateway gateway;private final ObjectMapper mapper;
 public ProductSearchService(KeyValueStore c,SearchKeyFactory k,ProductQueryGateway g,ObjectMapper m){cache=c;keys=k;gateway=g;mapper=m;}
 public CatalogPageResponse search(SearchCriteria c){String key=keys.key(c);var cached=cache.get(key);try{
  if(cached.isPresent())return mapper.readValue(cached.get(),CatalogPageResponse.class);
  var response=gateway.search(c);cache.put(key,mapper.writeValueAsString(response),Duration.ofSeconds(60));return response;
 }catch(com.fasterxml.jackson.core.JsonProcessingException e){throw new IllegalStateException("Cache serialization failed",e);}}
}

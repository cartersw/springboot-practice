package dev.practice.assessment02.cache;
import java.util.*;import java.nio.charset.StandardCharsets;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Component;
import dev.practice.assessment02.search.SearchCriteria;
@Component public class SearchKeyFactory {
 private final ObjectMapper mapper;public SearchKeyFactory(ObjectMapper m){mapper=m;}
 public String key(SearchCriteria c){try{
  var values=Arrays.asList(c.q(),c.category(),c.minPrice(),c.maxPrice(),c.inStock(),c.page(),c.size(),c.sort());
  return "products:search:v1:"+Base64.getUrlEncoder().withoutPadding().encodeToString(mapper.writeValueAsString(values).getBytes(StandardCharsets.UTF_8));
 }catch(Exception e){throw new IllegalStateException("Cannot encode search",e);}}
}

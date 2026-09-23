package dev.practice.assessment02.search;
import java.util.*;
import org.springframework.stereotype.Component;
import dev.practice.assessment02.error.InvalidRequestException;
@Component public class SearchRequestParser {
 private String text(String s,int max){if(s==null||s.strip().isEmpty())return null;String v=s.strip().toLowerCase(Locale.ROOT);if(v.length()>max)throw new InvalidRequestException("Search text too long");return v;}
 private Integer integer(Map<String,String> p,String key,int min,int max,Integer fallback){
  if(!p.containsKey(key))return fallback;
  try{String s=p.get(key).strip();if(!s.matches("[+-]?[0-9]+"))throw new NumberFormatException();int v=Integer.parseInt(s);if(v<min||v>max)throw new NumberFormatException();return v;}catch(Exception e){throw new InvalidRequestException("Invalid "+key);}
 }
 public SearchCriteria parse(Map<String,String> p){
  String q=text(p.get("q"),80),category=text(p.get("category"),40);
  Integer min=integer(p,"minPrice",0,1000000000,null),max=integer(p,"maxPrice",0,1000000000,null);
  if(min!=null&&max!=null&&min>max)throw new InvalidRequestException("Invalid price range");
  Boolean stock=null;if(p.containsKey("inStock")){String s=p.get("inStock").strip().toLowerCase(Locale.ROOT);if(!s.equals("true")&&!s.equals("false"))throw new InvalidRequestException("Invalid stock flag");stock=Boolean.valueOf(s);}
  SearchSort sort;try{sort=SearchSort.valueOf(p.getOrDefault("sort","priceAsc").strip());}catch(Exception e){throw new InvalidRequestException("Invalid sort");}
  return new SearchCriteria(q,category,min,max,stock,integer(p,"page",0,1000000,0),integer(p,"size",1,50,5),sort);
 }
}

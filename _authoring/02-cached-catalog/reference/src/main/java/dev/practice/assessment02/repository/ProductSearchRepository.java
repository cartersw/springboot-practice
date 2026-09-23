package dev.practice.assessment02.repository;
import java.util.*;
import jakarta.persistence.EntityManager;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;
import dev.practice.assessment02.model.Product;
import dev.practice.assessment02.search.*;
import dev.practice.assessment02.dto.*;
@Repository public class ProductSearchRepository {
 private final EntityManager em;public ProductSearchRepository(EntityManager em){this.em=em;}
 @Transactional(readOnly=true) public CatalogPageResponse search(SearchCriteria c){
  List<String> filters=new ArrayList<>();Map<String,Object> params=new HashMap<>();
  String q="locate(:q,lower(p.name)) > 0",category="lower(p.category) = :category";
  if(c.q()!=null&&c.category()!=null)filters.add("("+q+" and "+category+")");
  else if(c.q()!=null)filters.add(q);else if(c.category()!=null)filters.add(category);
  if(c.q()!=null)params.put("q",c.q());if(c.category()!=null)params.put("category",c.category());
  if(c.minPrice()!=null){filters.add("p.priceCents >= :min");params.put("min",c.minPrice());}
  if(c.maxPrice()!=null){filters.add("p.priceCents <= :max");params.put("max",c.maxPrice());}
  if(c.inStock()!=null)filters.add(c.inStock()?"p.stock > 0":"p.stock = 0");
  String where=filters.isEmpty()?"":" where "+String.join(" and ",filters);
  String order=switch(c.sort()){case priceAsc->"p.priceCents asc, p.id asc";case priceDesc->"p.priceCents desc, p.id asc";case nameAsc->"lower(p.name) asc, p.id asc";};
  var query=em.createQuery("select p from Product p"+where+" order by "+order,Product.class);
  var count=em.createQuery("select count(p) from Product p"+where,Long.class);
  params.forEach((k,v)->{query.setParameter(k,v);count.setParameter(k,v);});
  int selectedPage=c.page();
  var content=query.setFirstResult(selectedPage*c.size()).setMaxResults(c.size()).getResultList().stream().map(ProductResponse::from).toList();
  long total=count.getSingleResult();
  int pages=(int)((total+c.size()-1)/c.size());
  return new CatalogPageResponse(content,c.page(),c.size(),total,pages,c.page()==0,pages==0||c.page()>=pages-1);
 }
}

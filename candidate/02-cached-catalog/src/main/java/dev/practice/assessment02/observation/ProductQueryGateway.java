package dev.practice.assessment02.observation;
import org.springframework.stereotype.Component;
import dev.practice.assessment02.search.SearchCriteria;import dev.practice.assessment02.dto.CatalogPageResponse;import dev.practice.assessment02.repository.ProductSearchRepository;
@Component public class ProductQueryGateway {
 private final QueryProbe probe;private final ProductSearchRepository repository;
 public ProductQueryGateway(QueryProbe p,ProductSearchRepository r){probe=p;repository=r;}
 public CatalogPageResponse search(SearchCriteria criteria){probe.increment();return repository.search(criteria);}
}

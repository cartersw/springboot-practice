package dev.practice.assessment01.contract;
import dev.practice.assessment01.support.ApiTestSupport;
import org.junit.jupiter.api.Test;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static org.assertj.core.api.Assertions.assertThat;
public class SmokeTest extends ApiTestSupport {
 @Test void contextStarts(){assertThat(mvc).isNotNull();}
 @Test void healthResponds() throws Exception {mvc.perform(get("/health")).andExpect(status().isOk()).andExpect(content().json("{\"status\":\"UP\"}"));}
}

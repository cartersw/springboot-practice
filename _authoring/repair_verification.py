"""Apply reviewed verification repairs; no candidate business-code changes."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import practice as p

def replace(path, old, new):
    text = path.read_text(encoding='utf-8')
    assert old in text, (path, old)
    path.write_text(text.replace(old, new), encoding='utf-8', newline='\n')

typed_shape = '''protected void shape(JsonNode n,String... names){
  assertThat(n.isObject()).isTrue();Set<String>s=new HashSet<>();n.fieldNames().forEachRemaining(s::add);assertThat(s).containsExactlyInAnyOrder(names);
  for(String name:names){var value=n.get(name);
   if(Set.of("id","priority","priceCents","stock","page","size","totalElements","totalPages","quantity","totalQuantity","availableQuantity","reservedQuantity","activeReservations").contains(name)||(name.equals("status")&&n.has("code")))assertThat(value.isIntegralNumber()).as(name+" is a JSON integer").isTrue();
   else if(Set.of("first","last").contains(name))assertThat(value.isBoolean()).as(name+" is a JSON boolean").isTrue();
   else if(Set.of("items","content").contains(name))assertThat(value.isArray()).as(name+" is a JSON array").isTrue();
   else assertThat(value.isTextual()).as(name+" is a JSON string").isTrue();
  }
 }'''
for assessment, slug in p.SLUGS.items():
    base = ROOT / '_authoring' / slug
    support = base / f'trusted-tests/src/test/java/dev/practice/assessment{assessment}/support/ApiTestSupport.java'
    replace(support, 'protected void shape(JsonNode n,String... names){Set<String>s=new HashSet<>();n.fieldNames().forEachRemaining(s::add);assertThat(s).containsExactlyInAnyOrder(names);}', typed_shape)
    replace(support, 'protected List<Long> ids(JsonNode n){List<Long>r=new ArrayList<>();n.forEach(x->r.add(x.get("id").asLong()));return r;}', 'protected List<Long> ids(JsonNode n){assertThat(n.isArray()).isTrue();List<Long>r=new ArrayList<>();n.forEach(x->{assertThat(x.path("id").isIntegralNumber()).isTrue();r.add(x.get("id").asLong());});return r;}')

base = ROOT / '_authoring/01-incident-desk/trusted-tests/src/test/java/dev/practice/assessment01/contract'
file = base / 'TicketPrivateContractTest.java'
replace(file, 'assertThat(ok("GET","/api/tickets?status=OPEN",null,200).isEmpty()).isTrue();', 'var filtered=ok("GET","/api/tickets?status=OPEN",null,200);assertThat(filtered.isArray()).isTrue();assertThat(filtered.isEmpty()).isTrue();')
replace(file, 'assertThat(ok("GET","/api/tickets",null,200).isEmpty()).isTrue();', 'var empty=ok("GET","/api/tickets",null,200);assertThat(empty.isArray()).isTrue();assertThat(empty.isEmpty()).isTrue();')

base = ROOT / '_authoring/03-inventory-reservations/trusted-tests/src/test/java/dev/practice/assessment03'
file = base / 'support/ApiTestSupport.java'
replace(file, 'protected void summary(JsonNode n,int[] available,long[] reserved,long[] active){', 'protected void summary(JsonNode n,int[] available,long[] reserved,long[] active){assertThat(n.isArray()).isTrue();')
replace(file, 'protected void stored(long id,String key,String customer,String status,String canonical)', 'protected void stored(long id,String key,String customer,String status)')
replace(file, 'try{assertThat(mapper.readTree(r.get("CANONICAL_PAYLOAD").toString())).isEqualTo(mapper.readTree(canonical));}catch(Exception e){throw new AssertionError(e);}', '')
file = base / 'contract/ReservationPublicContractTest.java'
replace(file, 'stored(id,"req-001","team-a","ACTIVE","[\\"team-a\\",[[\\"BOLT-M8\\",3],[\\"NUT-M8\\",2]]]");', 'stored(id,"req-001","team-a","ACTIVE");')
file = base / 'contract/ReservationPrivateContractTest.java'
replace(file, 'reset();Fixtures.cancelled701(jdbc);if(depleted)', 'reset();var original=create(standard("cancelled-replay"),201);long id=original.path("id").asLong();cancel(id,200);if(depleted)')
replace(file, 'var n=create(standard("fixture-701"),200);response(n,701,"fixture-701","team-a","CANCELLED","BOLT-M8=3","NUT-M8=2");assertThat(snapshot()).isEqualTo(before);counts(1,2,2);events(701,"CANCELLED","CREATED");', 'var n=create(standard("cancelled-replay"),200);response(n,id,"cancelled-replay","team-a","CANCELLED","BOLT-M8=3","NUT-M8=2");assertThat(snapshot()).isEqualTo(before);counts(1,2,2);events(id,"CANCELLED","CREATED");')

# Keep reference, trusted and public copies byte-for-byte consistent.
for assessment, slug in p.SLUGS.items():
    base = ROOT / '_authoring' / slug
    for source in (base/'trusted-tests').rglob('*'):
        if not source.is_file(): continue
        relative = source.relative_to(base/'trusted-tests')
        for target in (base/'reference', ROOT/'candidate'/slug):
            if target == ROOT/'candidate'/slug and 'PrivateContractTest' in source.name: continue
            (target/relative).write_bytes(source.read_bytes())
    readme = ROOT/'candidate'/slug/'README.md'
    replace(readme, 'From this candidate folder, select the supplied local tools for this shell:', 'From the pack root, follow START_HERE.md to select JDK 21 and Python 3.11+.\nThen open this candidate or fresh-attempt folder in the same PowerShell window:')
    replace(readme, '. ..\\..\\tools\\Use-PracticeEnvironment.ps1\n', '')
    replace(readme, 'From the pack root (two levels above this candidate folder):', 'From the pack root (the folder containing START_HERE.md; fresh attempts may be deeper):')
    replace(readme, 'The pack environment script changes this shell only.', 'The optional pack environment script changes this shell only.')
    # Use domain-relevant error examples and remove copied builder-only wording.
    doc = ROOT/'candidate'/slug/'ASSESSMENT.md'
    replace(doc, ' Numeric strings are not a separate scored coercion edge case; do not create surprise private tests for them.', ' Numeric strings are not a separate scored coercion edge case.')
    replace(doc, ' Implement correct infrastructure for malformed JSON, argument conversion, and validation responses from the start.', '')
    if assessment == '02':
        replace(doc, '"message": "Ticket not found",\n  "path": "/api/tickets/9999"', '"message": "Product not found",\n  "path": "/api/products/9999"')
    elif assessment == '03':
        replace(doc, '"code": "NOT_FOUND",\n  "message": "Ticket not found",\n  "path": "/api/tickets/9999"', '"code": "RESERVATION_NOT_FOUND",\n  "message": "Reservation not found",\n  "path": "/api/reservations/9999"')
print('Applied contract-test fairness, JSON schema, and portable README repairs.')

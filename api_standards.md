API Standards
=============

API Coding Standards
--------------------

### Response Codes

*   Use Constants for response types (e.g., StatusCodes.Status200OK).
    
*   All possible responses should be spelled out for each API call.
    
*   GET/POST/PUT/DELETE.
    
*   Invalid inputs of any kind should return 400 Bad Request.
    
*   Server errors of any kind should return 500 - Internal Server Error.
    

**GET**

*   Single object, object found - 200 - OK.
    
*   List of objects, 1 or more returned - 200 OK.
    
*   List of objects, empty list returned - 204 - No Content.
    

**POST**

*   Object inserted, void return type - 204 - No Content.
    
*   Object inserted, non-void return type - 201 - Created.
    

**PUT**

*   Object updated, void return type - 204 - No Content.
    
*   Object updated, non-void return type - 200 - OK.
    

**DELETE**

*   Success, void return type - 204 - No Content.
    

### RESTful CRUD Methods

*   **GET** - Used to retrieve information.
    
*   **POST** - Used to create a new entity.
    
*   **PUT** - Used to update an entity.
    
*   **DELETE** - Used to delete an entity.
    

### RPC Style for Executing Processes

*   URI path format: /PH/{logical-group}/{entity}/{id?}.
    
    *   Example: /PH/property/units/1.
        
    *   Example: /PH/property/properties/5.
        
*   The entity should be plural. Think of it like a collection with an index, e.g., properties\[5\].
    
*   If there are multiple parameters being passed, each parameter should be passed after the appropriate entity in the path name.
    
    *   Example: GET/PH/property/properties/19/buildings/23/units/4/residents returns all residents residing in Unit 4 of Building 23 of Property 19.
        
*   Use both the logical path and entity even if they appear redundant.
    
    *   Good: PH/household/households/{householdID}/.
        
    *   Bad (omits the entity): PH/household/{householdID}/.
        
    *   Bad (improperly indexes logical group, omits logical group "household"): PH/households/{householdID}/.
        
*   Avoid using verbs in URI path. The GET/POST/PUT/DELETE methods give the action being done on the object represented by the path. There is no need to include phrases like "get", "add", "update", "delete", etc..
    
*   Use status codes to indicate errors vs. success.
    
*   Validation and Errors - TBD - link to validations standards doc.
    

### Controllers

*   Keep as simple as possible.
    
*   Avoid unnecessary duplication.
    
*   Maintain good code placement.
    
*   Just because certification needs the information does not mean it belongs in the certification controller area.
    
*   Uses DTOs as results and Models to interact with the services.
    
*   Has references to services as needed through DI.
    
*   Lightweight and mainly a passthrough to service methods.
    
*   Under development - Add logging to controller methods.
    
    *   We need standards for determining exactly what events get logged and what log messages include.
        
*   Use CreatedAtRoute() with nameof() rather than Created() for add (POST) operations. This avoids hardcoding the path to the created resource. See nameof documentation.

Example
```
[HttpGet("/PH/contracts/affordableHapContracts/{affordableHapContractID}")]
[ProducesResponseType(typeof(AffordableHapFundingProgramContractDto), StatusCodes.Status200OK)]
public IActionResult GetByAffordableHapContractID(int affordableHapContractID) {
  var result = _service.GetAffordableDetails(affordableHapContractID);
  Ok(result.ToAffordableHapFundingProgramContractDto());
}

//Add uses CreatedAtRoute to point to GET path's Name
[HttpPost("/PH/contracts/affordableHapContracts/")]
[ProducesResponseType(typeof(int), StatusCodes.Status201Created)]
public IActionResult AddAffordableHapContract([FromBody] AffordableHapFundingProgramContractDto contract) {
  //insert logic here
  return CreatedAtRoute(
    nameof(GetByAffordableHapContractID),
    new { affordableHapContractID = result.ContractDetailID },
    result.ContractDetailID
  );
}
```
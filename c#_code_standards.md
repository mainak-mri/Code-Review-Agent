# C♯ Standards

## C# Coding Standards

## Overall Clean Code Standards

```
Single Responsibility Principle - A class should have one and only one reason to change.
Open Closed Principle - Classes should be open for extension and closed for modification.
Liskov Substitution Principle - Derived classes must be substitutable for their base classes.
Interface Segregation Principle - Make fine grained interfaces that are client specific.
Dependency Inversion Principle - Depend on abstractions, not on concrete implementations.
```
```
The behavior of a class or method should match its name
There should be no surprises
Don't use abbreviations to shorten names with the exception of industry standards
e.g. HUD, RFTA, USDA, HAP, etc.
Don't be afraid to use longer, more expressive names within reason
Examples:
```
```
Needing to pass this many parameters is a sign of bad code design (it's a code smell)
Try to restructure your code to use a structure or class to group the parameters together and pass
them as a single argument instead of passing multiple arguments
If the parameters are not closely related enough to group into a structure or class, consider
refactoring the method or breaking it into multiple smaller, more concise methods that require fewer
parameters
```
```
The point is to make the class easy to read and see everything at a glance
Split at good logical areas
```
```
Keep your classes small and your methods smaller
```
```
Use editor.config for formatting
```
```
Don't inject Scoped or Transient services into a Singleton service, also don't inject Transient services into
a Scoped service
```
```
Follow the SOLID principles
```
```
Use descriptive names for your classes, methods, and variables that express their behavior
```
```
sfnFixSelect() -> EscapeSQLParameter()
LicFresh() -> LicenseRefresh()
fnGetUserLicAss() -> GetUserLicenseAssociations()
```
###

```
Avoid creating methods that take more than 3 arguments
```
```
Ensure that each line of code can fit on a standard monitor (without scrolling)
```

```
Always write unit tests for all your code
If you cannot figure out how to test a piece of code, ask a senior developer for assistance or start a
team discussion
These are great opportunities to learn new testing techniques
```
```
They are indicators of non-expressive code
If you need a comment to make the meaning of a method or class clear, consider renaming or
restructuring the code to make it express its behavior to the reader
If you are unsure if your code is clear enough, get another developer to take a look at it and have
them explain the behavior to you as they read through it. If they struggle to understand any lines (or
even worse, they say something wrong), you should try to improve the readability/expressiveness. Ask
them if they have any suggestions.
```
```
If you are hiding code within a region, it is a sign that your code is too long or poorly structured
Each line of code should be important enough to be visible to the reader
```
```
Do not scatter member variable declarations throughout the methods/properties/constructors/fields
in the class
Use keyword "var" when defining variables data types whenever possible
```
```
For example, place all constants together, all private instance variables together, all properties
together, all constructors together, and all methods together
Data members, Constructor, Public, Protected, Private
```
```
On the other extreme, code with no whitespace requires additional effort to determine related lines
and the beginnings and ends of methods
Group related lines of code vertically closer together than unrelated lines of code
Do not be afraid to add a blank line in a method to act as a logical separation of ideas
Above all, be consistent! Having inconsistent vertical whitespace makes code harder to scan. It can
lead to false impressions of the structure of code and require more effort to read/understand.
```
```
Fields cannot be included in interfaces, hence can't be mocked in a unit test
Future requirements may require you to add validation around getting/setting the piece of data -
changing from a field to a property may be a breaking change for some consumers of your class,
```
Don't use magic numbers. Never hard-code a numeric or string value that isn't meant to be shown to the
user. Instead, declare a constant or enumeration with a descriptive name.

Untested code is not clean!

Use comments sparingly

Never use regions!

All member/instance variables should be declared at the top of their containing class

Contents of a class should be grouped together by their type

Be smart about whitespace! Don't include more than one line of vertical whitespace between lines of code
or methods (eg. 4 lines of whitespace between methods, or 3 lines of code between the last line of code in
a method and the closing "End Function" or curly brace).

Expose class state through properties instead of through public fields. There are a few reasons for this:


```
depending on their usage
Exposing fields directly breaks the OOP principle of encapsulation. Data in an exposed field can be
modified by any consumer of your class.
```
## File Naming Standards and Project/Solution Organization

```
Use class name for file name
For example, a source file which contains the class Lease would be named Lease.cs. One class or
interface per file.
Use Pascal case and very descriptive names
Do not use abbreviations. (i.e. Adjustment not Adj)
When using acronyms:
Use Pascal case for acronyms more than two characters long
e.g HtmlButton instead of HTMLButton
Capitalize acronyms that consist of only two characters
e.g. System.IO instead of System.Io
Capitalize ID in ID fields
e.g. PropertyID
Same rule as above, well known and industry wide acronyms are acceptable
A basic definition of "well known" for the industry could be if it is found throughout HUD documentation
which can often be found out via a google search
```
## Structure

Services (Business Layer)

```
Input/output using Models to Controllers
Has references to single Repository as needed through DI
To group repository calls under one transaction you can use Transaction.InTransaction() which takes a
lambda function where you should call all of the repository methods needed
Services should not have a dependency tree deeper than 15
For example ServiceA depends on ServiceB and ServiceC and ServiceC depends on ServiceD.
ServiceA has a dependency tree depth of 2, ServiceC has a depth of 1, and ServiceB and ServiceD
have depths of 0.
```
Repositories

```
Details on standards in a separate page
```
DTOs

```
POCO objects used to pass data back and forth from UI to Controllers
DTOs should be modeled after the UI/process
Complex screens may require complex/composite DTOs. Try to reference and use other DTOs only when it
makes sense.
i.e. if it's not obvious, just roll your own. Would rather have "duplicate" code than try to maintain
complex web of DTOs at this point
```

```
DTO fields will be named based on need, but generally should be Pascal case with no abbreviation
DTO fields that reference a primary key or foreign key field should follow the same guidance as below for
domain model PKs/FKs
```
Domain Models

```
Under review - POCO objects used in the Service layer to essentially abstract implementation of database
tables and have a .NET class to perform business logic with
This standard is under review.
If you come across an example where it would be useful to include logic in the domain model, bring it
up to the teams/leads to decide whether it makes sense.
Under review - No parent/child object graphs (i.e. a model should not contain a reference to another
model)
This standard is under review.
If you come across an example where it would be useful to include child objects in the domain model,
bring it up to the teams/leads to decide whether it makes sense.
The service code will need to instantiate/populate separate "child" objects as needed
Model and field names do not need to match database names exactly. (RMBLDGID should be
RMBuildingID)
Meaningful, plain-English class and property names should be used. Example:
```
**Primary and Foreign Key properties**

```
Should not be nullable, 0 can be used to denote that the value has not been specified
If database table has primary key identity field for model, just use ID
Should be first member of class.
```
```
If database has compound or multiple keys: Specify each key with descriptive name (e.g., RMPropID and
RMBLGD and UNITID)
```
```
//Database table and fields
// dbo.NAME
// MIDINIT
// LEASAGID
// NOLATE
public class ResidentModel {
public char MiddleInitial { get; set; }
public string LeasingAgentID { get; set; }
public int NumberOfLatePayments { get; set; }
}
```
###

```
public class WaitingListModel {
public int ID { get; set; }
...
}
```
###


```
If model property holds foreign key ID of object, use a description of the referenced table with "ID" suffix.
```
**Mappers**

```
Use SafeRow in all methods interacting with Row
Row Get___() functions return default value for their data types
Use GetNullable___() functions if the column is nullable and null is expected/valid value
```
**Controllers**

```
Controllers should not depend on more than 30 total objects including implied dependencies
For example Controller1 depends on ServiceA, ServiceA depends on ServiceB and ServiceC, and
ServiceC depends on ServiceD. Controller1 depends on a total of 4 objects (all 4 services) despite
only declaring a single dependency (ServiceA).
```
```
public class PropertyModel : ModelBase {
public int ID { get; set; }
public string RMPropertyID { get; set; }
public string RMBuildingID { get; set; }
public string RMUnitID {get; set;}
...}
```
###

```
public class WaitingListModel {
public int ID { get; set; } //primary key
public string Name { get; set; }
public int WaitingListStatusGroupID { get; set; } //foreign key
...
}
```
### 
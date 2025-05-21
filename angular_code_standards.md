# Angular Standards

## Angular Coding Standards

## File/Folder Structure

```
Trying to adhere to most of the general structure guidelines from angular docs:
Each feature area resides in its own folder.
Each feature has its own Angular feature module.
Feature area routes rarely (if ever) cross with routes of other features.
The structure should be designed/maintained with lazy-loading and overall bundle size in mind
Each feature module will contain
a feature module file (i.e. feature.module.ts)
a feature-level routing file will be created that performs routing for routes directed to it by app-level
routing (i.e. feature-routing.module.ts)
a "views" folder (currently pages) to store the view components (items that are loaded by routes)
(Container Component )
a "containers" folder (currently does not exist) - getting, loading, changing data
a "presentations" folder (currently components) to store any reusable components within the module
(Presentational Component )
a "services" folder to store services only used within the module
a "models" folder to store classes that are only used within the module
a "state" folder for NgRx state management (optional)
a "enums" folder for enum types specific to the module (optional)
a "directives" folder for @Directive specific to the module (optional)
a "pipes" folder for @Pipe specific to the module (optional)
Every file should be doing only one thing such as a service or component, per file. This also includes and
means that Enums should be in their own separate files
Don't be afraid to break a big file out into smaller more manageable files if it makes sense.
Create folders for generic components
Consider creating sub-folders when a folder reaches seven or more files
File names should be kebab-case
```
## Typescript

```
Don't let functions be super long. Make smaller functions as it makes sense
Do use single quotes
Do explicitly type all of your properties and variables except when setting them to something on creation if
it is automatically inferred
```
**Follow the official Angular Style Guide with a few exceptions noted below. Some bullets points are
already stated in the official study guide, but are noted again here to avoid any potential confusion.**

https://angular.io/guide/styleguide


```
Reusable (presentational) components should prefix the selector with 'mri-ph'
Selector should not be needed for container components (./pages), only components used in html
templates
Order of File. Number one determines that it should go at the top within with given class and other
numbers follow below that. On top of that, within each number group them by public, protected, and
private. Public being at the top and private being at the bottom
```
1. Import statements
2. Inputs/outputs/viewchildren/angular property things
3. Properties
4. Constructor
5. Angular Lifecycle Hooks
6. Methods
    Import section
       Use 'Organize Imports' in VS Code to sort the imports

```
if there is line length error
```
```
change to multiline import
```
```
Avoid using * to import all functions, classes, enums, etc. Each item should be specified in the import
statement
Use relative paths
Do avoid using the any type when possible and try to type a variable to something specific
Do name events without the prefix 'on'. Don't prefix output properties
```
## HTML

```
Do not put logic in templates. Put them in appropriate functions
Always prefer using [class.your-classname]="expression" versus [ngClass]="{ 'your-classname': expression }"
```
## Pendo

```
New UI elements should have Pendo tags in most cases
Refer to Jira card for Pendo verbiage.
```
## Coding Conventions


```
2 space indentation
One extra line at the end of files (tslint default)
For functions and methods, if there are over three arugments, separate them by putting one argument per
line. Three arguments on one line is OK, depending on line length.
```
## Exceptions to the Angular Style Guide

## Typescript

```
Do explicitly state return types for your methods. Don't do this for the constructor, Angular Lifecycle
Hooks, and other Angular specific things. No need to specify return types for 'void' methods (no return
object).
Don't worry about things being in alphabetical order
Variable names and functions should be camelCase (exception to style guide below)
Private data members should be prefixed with '_'
private _camelCase: string
Observables should be suffixed with $
camelCase$: Observable<boolean>;
Do give the filename the conventional suffix (such as .directive.ts, .module.ts, .pipe.ts, or .service.ts) for a file
of that type.
We are not adding a conventional suffix for models (i.e. *.model.ts)
```
## Temporary Boyscout Items

```
Fix any file name that is not following kebab-case (use TFS rename)
i.e. tenantVoucher.ts should be tenant-voucher.ts
We should also consider breaking out nested file structures rather than burying too deep
Do not repeat the parent folder as in certification/certification-hud50058 should be certification/hud
```
### constructor(private _ownerAgentService: OwnerAgentService, private _messageService: MessageService) { } 

```
constructor(private _router: Router,
private _messageService: MessageService,
private _voucherProjectService: VoucherProjectService,
private _voucherApplicationService: VoucherIssuanceService,
private _store: Store<State>) { }
```
### 
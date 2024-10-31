## LDAP

- What
  - Lightweight Directory Access Protocol
  - a protocol
  - to access directory information
  - client connect over TCP/IP
  - allow communication with directory service
- Directory services
  - Microsoft Active Directory
  - OpenLDAP
  - LDAP compatible servers
- Data storage

  - hierarchical structure called DIT (Directory Information Tree)
  - each entry has unique id
  - hierarchy represents org or geographical division
  - example

  ```
  -> Root(top of the tree)
    -> Country(C): c=us
        -> Organization(O): o=Galaxy
            -> Organizational Unit(OU):
                -> ou=People
                    -> user entries: uid=jhon.doe, uid=badal.sarkar
                -> ou=Groups
                    -> Group entries: cn=developers, cn=admins
                -> ou=Devices
                    -> Device entries: cn=laptop1, cn=printer02
  ```

  - components
    - DN (Distinguished Name)
      - each entry has a unique DN
      - specifies the specific location in the tree
      - above example DN for jhon.doe is `uid=jhon.doe,ou=people,o=Galaxy,c=US`
    - Attributes
      - Each entry has attributes e.g. uid, cn(common name), email, telephoneNumber etc.
      - What attributes an entry can have depends on the object classes
    - Object classes
      - defines schema for entries
      - defines which attributes are required and optional

**example user entry**

```yaml
dn: uid=john.doe,ou=People,o=ExampleCorp,c=US
uid: john.doe
cn: John Doe
sn: Doe
mail: john.doe@example.com
telephoneNumber: +1 555 0101
objectClass: inetOrgPerson
```

**example group entry**

```yaml
dn: cn=developers,ou=Groups,o=ExampleCorp,c=US
cn: developers
objectClass: groupOfNames
member: uid=john.doe,ou=People,o=ExampleCorp,c=US
member: uid=alice.smith,ou=People,o=ExampleCorp,c=US
```

# quizrt
Real Time Quiz project

# Learned in this project (2020 retrospective)

include your team. don't be a superman. we on the backend collaborated and it went great, but the front end team had one guy who got completely steamrolled. 
We could have adopted him to the back end and given him something to learn and do, but we didn't find out about it until the night of the release.
There would have definitely been some team re-structuring if that had been a commercial project.

## Graphene-Django
### Building django models
primitive field types as well as FKs
lifecycle hooks (onSave/onDelete) can be perfect times to handle certain validations and maintenance tasks. CRUD of one object might neccessitate the CRUD of others.

### Django DB objects filteringn in logic
syntax such as *.objects.filter(pk__in=(stuff))

### Django forms
can indicate which fields of a Model are used in what way. ie: filter_fields, exclude_fields

### Fixtures
A dump for test data

### Speaking of test data...
we didn't test this worth beans. If you pick this back up and dust it off, please write tests.

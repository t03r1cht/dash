### Upcoming:
After the release of Dash 1.0 begin work on Flash, which is a lightweight, open source image board software.

### Database Structure

#### Table `dash_users`

- uid:`int` (Primary Key)
- username:`varchar(100)`
- email:`varchar(250)`
- password:`varchar(150)`
- creation_date:`datetime`
- role_id:`int`
- profile_data:`varchar(5000)`

#### Table `dash_users_verification`

- uid:`int` (Foreign Key -> `dash_user.uid`)
- verified:`boolean`
- token:`varchar(50)`
- verification_date:`datetime`

#### Table `dash_roles`
- role_id:`int`
- name:`varchar(100)`
- config_board:`boolean`

### Section Preview Structure

```python
    section_list = [
        {
            "title": "General",
            "section_preview": [{
                "name": "Welcome to the Dash Board...",
                "info": "Count: 1"
            },
                {
                    "name": "This is the first thread on the Dash Board...",
                    "info": "Count: 10"
                }]
        },
        {
            "title": "Announcements",
            "section_preview": [{
                "name": "Welcome to the Dash Board...",
                "info": "Count: 1"
            },
                {
                    "name": "his is the first thread on the Dash Board...",
                    "info": "Count: 10"
                }]
        }
    ]
```
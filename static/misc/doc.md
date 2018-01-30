### Upcoming:
After the release of Dash 1.0 begin work on Flash, which is a lightweight, open source image board software.


### To Do

- @before_request decorator to check if the user is authenticated
- Implement brute force protection
- Implement password reset
- Implement password change and email change

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

#### Table `dash_forum_sections`

- section_id:`int`
- section_name:`varchar(150)`
- section_creation_date:`datetime`

#### Table `dash_forum_subsections`

- subsection_id:`int`
- section_id:`int`(Foreign Key -> `dash_forum_sections.section_id`)
- subsection_name:`varchar(150)`
- subsection_desc`varchar(250)`
- subsection_creation_date:`datetime`

#### Table `dash_forum_threads`
- thread_id:`int`
- subsection_id:`int` (Foreign Key -> `dash_forum_subsections.subsection_id`)
- thread_title:`varchar(250)`
- thread_creator:`int` (Foreign Key -> `dash_users.uid`)
- thread_views:`int`
- thread_replies:`int`
- thread_status:`varchar(50)`
- thread_creation_date:`datetime`


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

### Profile JSON Structure

The entire profile data for a user will be stored in the `profile_data` column of the `dash_users` table.

```python
{
    "username":"quazee",
    "register_date":"01-01-1990 21-20-20",
    
}
```





























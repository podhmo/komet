komet
========================================

models.py

::

    members_to_teams = sa.Table(
        "members_to_teams", Base.metadata,
        sa.Column("member_id", sa.Integer, sa.ForeignKey("members.id")),
        sa.Column("team_id", sa.Integer, sa.ForeignKey("teams.id")),
    )


    class Member(Base):
        __tablename__ = "members"
        id = sa.Column(sa.Integer, primary_key=True)
        name = sa.Column(sa.String(255), nullable=False)
        created_at = sa.Column(sa.DateTime())
        teams = orm.relationship("Team", backref="members", secondary=members_to_teams)


    class Team(Base):
        __tablename__ = "teams"
        id = sa.Column(sa.Integer, primary_key=True)
        name = sa.Column(sa.String(255), nullable=False)
        created_at = sa.Column(sa.DateTime())


configuration

::

    def inludeme(config)
        config.include("komet")
        config.komet_initialize(config.maybe_dotted(".models.Base"),
                                config.maybe_dotted(".models.DBSession"),
                            )
        config.add_komet_apiset(config.maybe_dotted(".models.Member"), "members", prefix="/api)
        config.add_komet_apiset(config.maybe_dotted(".models.Team"), "teams", prefix="/api)

add views automatilcally, such as below.

- listing
- creation
- editing
- deletion
- add child
- remove child
- (schema information)

::

    $ pviewlist development.ini

                      Path                   Method         View        
    --------------------------------------------------
    static/*subpath                          -      pyramid.static:static_view
    /api/members/schema/                     GET    komet.views:schema  
    /api/members/                            GET    komet.views:listing 
    /api/members/                            POST   komet.views:create  
    /api/members/{id}/                       GET    komet.views:show    
    /api/members/{id}/                       PUT    komet.views:edit    
    /api/members/{id}/                       DELETE komet.views:delete  
    /api/members/{id}/teams/                 GET    komet.views:listing_children
    /api/members/{id}/teams/                 POST   komet.views:create_child
    /api/members/{id}/teams/{child_id}/      PUT    komet.views:add_child
    /api/members/{id}/teams/{child_id}/      DELETE komet.views:remove_child
    /api/teams/schema/                       GET    komet.views:schema  
    /api/teams/                              GET    komet.views:listing 
    /api/teams/                              POST   komet.views:create  
    /api/teams/{id}/                         GET    komet.views:show    
    /api/teams/{id}/                         PUT    komet.views:edit    
    /api/teams/{id}/                         DELETE komet.views:delete  
    /api/teams/{id}/members/                 GET    komet.views:listing_children
    /api/teams/{id}/members/                 POST   komet.views:create_child
    /api/teams/{id}/members/{child_id}/      PUT    komet.views:add_child
    /api/teams/{id}/members/{child_id}/      DELETE komet.views:remove_child

schema information

::

    # /api/teams/schema/
    {
      "title": "Team",
      "type": "object",
      "properties": {
        "id": {
          "type": "integer"
        },
        "name": {
          "maxLength": 255,
          "type": "string"
        },
        "created_at": {
          "format": "date-time",
          "type": "string"
        }
      },
      "required": [
        "id",
        "name"
      ],
      "links": [
        {
          "href": "/api/teams/schema/",
          "rel": "self",
          "title": "getting schema information of Team",
          "method": "GET",
          "encType": "application/json",
          "mediaType": "application/json"
        },
        {
          "href": "/api/teams/",
          "rel": "self",
          "title": "list Team objects",
          "method": "GET",
          "encType": "application/json",
          "mediaType": "application/json"
        },
        {
          "href": "/api/teams/",
          "rel": "self",
          "title": "create Team object",
          "method": "POST",
          "encType": "application/json",
          "mediaType": "application/json"
        },
        {
          "href": "/api/teams/{id}/",
          "rel": "self",
          "title": "detail information about Team object",
          "method": "GET",
          "encType": "application/json",
          "mediaType": "application/json"
        },
        {
          "href": "/api/teams/{id}/",
          "rel": "self",
          "title": "edit Team object",
          "method": "PUT",
          "encType": "application/json",
          "mediaType": "application/json"
        },
        {
          "href": "/api/teams/{id}/",
          "rel": "self",
          "title": "delete Team object",
          "method": "DELETE"
        },
        {
          "href": "/api/teams/{id}/members/",
          "rel": "self",
          "title": "listing children of Team object",
          "method": "GET",
          "encType": "application/json",
          "mediaType": "application/json"
        },
        {
          "href": "/api/teams/{id}/members/",
          "rel": "self",
          "title": "create object as members of Team's children",
          "method": "POST",
          "encType": "application/json",
          "mediaType": "application/json"
        },
        {
          "href": "/api/teams/{id}/members/{child_id}/",
          "rel": "self",
          "title": "take part in a members of Team's children",
          "method": "PUT",
          "encType": "application/json",
          "mediaType": "application/json"
        },
        {
          "href": "/api/teams/{id}/members/{child_id}/",
          "rel": "self",
          "title": "remove from members of Team's children",
          "method": "DELETE"
        }
      ]
    }


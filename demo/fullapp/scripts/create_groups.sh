#!/bin/bash
TARGET="http://localhost:6543/groups/"
METHOD="POST"
DATA=`cat <<EOF
{
  "name": "Foo"
}
EOF
`

curl -d "${DATA}" -X "${METHOD}" "${TARGET}"

TARGET="http://localhost:6543/groups/"
METHOD="POST"
DATA=`cat <<EOF
{
  "name": "Boo"
}
EOF
`

curl -d "${DATA}" -X "${METHOD}" "${TARGET}"

TARGET="http://localhost:6543/users/"
METHOD="POST"
DATA=`cat <<EOF
{
  "group_id": 1,
  "name": "x"
}
EOF
`

curl -d "${DATA}" -X "${METHOD}" "${TARGET}"

TARGET="http://localhost:6543/users/"
METHOD="POST"
DATA=`cat <<EOF
{
  "group_id": 1,
  "name": "y"
}
EOF
`

curl -d "${DATA}" -X "${METHOD}" "${TARGET}"

TARGET="http://localhost:6543/users/"
METHOD="POST"
DATA=`cat <<EOF
{
  "group_id": 1,
  "name": "z"
}
EOF
`

curl -d "${DATA}" -X "${METHOD}" "${TARGET}"



import os

import pytest

from tartiflette.engine import Engine
from tartiflette.schema import GraphQLSchema

_curr_path = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.asyncio
async def test_tartiflette_engine_initialization_with_sdl_file_list():
    engine = Engine(
        [
            _curr_path + "/data/splitted_sdl/author.sdl",
            _curr_path + "/data/splitted_sdl/blog.sdl",
            _curr_path + "/data/splitted_sdl/post.sdl",
            _curr_path + "/data/splitted_sdl/query.sdl",
        ]
    )

    assert engine.schema.find_type("Author") is not None
    assert engine.schema.find_type("Blog") is not None
    assert engine.schema.find_type("Post") is not None
    assert engine.schema.find_type("Query").find_field("blogs") is not None


@pytest.mark.asyncio
async def test_tartiflette_engine_initialization_with_sdl_folder():
    engine = Engine(_curr_path + "/data/splitted_sdl")

    assert engine.schema.find_type("Author") is not None
    assert engine.schema.find_type("Blog") is not None
    assert engine.schema.find_type("Post") is not None
    assert engine.schema.find_type("Query").find_field("blogs") is not None


@pytest.mark.asyncio
async def test_tartiflette_engine_initialization_with_single_sdl_file():
    engine = Engine(_curr_path + "/data/simple_full_sdl/simple_full.sdl")

    assert engine.schema.find_type("Author") is not None
    assert engine.schema.find_type("Blog") is not None
    assert engine.schema.find_type("Post") is not None
    assert engine.schema.find_type("Query").find_field("blogs") is not None


@pytest.mark.asyncio
async def test_tartiflette_engine_initialization_by_passing_schema():
    schema = GraphQLSchema()
    schema._gql_types["test"] = "test"
    engine = Engine(schema)

    assert engine.schema.find_type("test") == "test"


@pytest.mark.asyncio
async def test_tartiflette_engine_initialization_with_string_schema():
    engine = Engine(
        """
    type Post {
        id: ID!
        title: String!
        publishedAt: Int!
        likes: Int! @default(value: 0)
        author: Author! @relation(name: "Posts")
        blog: Blog @relation(name: "Posts")
    }

    type Author {
        id: ID!
        name: String!
        posts: [Post!]! @relation(name: "Author")
    }

    type Blog {
        id: ID!
        name: String!
        description: String,
        authors: [Author!]!
        posts: [Post!]! @relation(name: "Posts")
    }

    type Query {
        authors: [Author!]!
        blogs: [Blog!]!
    }
    """
    )

    assert engine.schema.find_type("Author") is not None
    assert engine.schema.find_type("Blog") is not None
    assert engine.schema.find_type("Post") is not None
    assert engine.schema.find_type("Query").find_field("blogs") is not None
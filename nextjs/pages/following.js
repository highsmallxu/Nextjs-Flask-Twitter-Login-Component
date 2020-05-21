import fetcher from "../libs/fetcher";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import Image from "react-bootstrap/Image";
import Head from "next/head";

function Following({ data }) {
  const followings = data.followings;

  return (
    <div>
      <Head>
        <title>Create Next App</title>
        <link rel="icon" href="/favicon.ico" />
        <link
          rel="stylesheet"
          href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
          integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh"
          crossorigin="anonymous"
        />
      </Head>
      <Container fluid="md" className="container-margin">
        <h3>Following</h3>
        <Row>
          {followings.map((f) => {
            return (
              <Col md={3} sm={12}>
                <Card>
                  <Card.Header>
                    <Image src={f.img} rounded style={{ width: 50 }} />
                  </Card.Header>
                  <Card.Body>
                    <Card.Title>{f.name}</Card.Title>
                    <Card.Text>{f.description}</Card.Text>
                  </Card.Body>
                </Card>
              </Col>
            );
          })}
        </Row>
      </Container>
    </div>
  );
}

export async function getServerSideProps({ query }) {
  const followings = await fetcher(
    "http://127.0.0.1:5000/access_token?oauth_token=" +
      query.oauth_token +
      "&oauth_verifier=" +
      query.oauth_verifier
  );
  return {
    props: {
      data: followings,
    },
  };
}

export default Following;

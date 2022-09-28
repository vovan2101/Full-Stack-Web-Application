import Navbar from "./components/Navbar";
import {useState, useEffect} from 'react'


function App() {

  const [articles, setArticles] = useState([])

  useEffect(() => {
    fetch('http://localhost:3000/get', {
      'method': 'GET',
      headers: {
        'Content-Type':'application/json'
      }
    })
    .then(resp => resp.json())
    .then(resp => console.log(resp))
    .catch(error => console.log(error))
  },[])

  return (
    <>
  <Navbar />
  </>
  );
}

export default App;

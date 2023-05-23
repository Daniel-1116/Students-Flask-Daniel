
// function Message() {
//     const [message, setMessage] = React.useState([]);

//     const getData = () => {
//         axios.get("/messages").then(response => {
//             setMessage(response.data);
//         })
//     };
//     React.useEffect(() => {
//         getData();
//     },[]
//     )
      
//     return (<div>
//         {message.slice(-2).map((item) =>
//             <h4>{item.msg}</h4>)}
//             <button onClick={getData}>Show New Messages</button>

//     </div>
//     )
// }
// ReactDOM.render(<Message/>, document.getElementById("msg"));

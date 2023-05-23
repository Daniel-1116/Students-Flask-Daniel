// function NewMessages(props) {
//     const [counter, setCounter] = React.useState(0);

//     const getData = () => {
//         axios.get("/newMessages").then(response => {
//             setCounter(response.data.counter);

//         })
//     };
//         React.useEffect(() => {
//             getData();
//             setInterval(getData,props.interval)
//         },[]
//         )
    
//     return (<div>
//                 <h3>You have {counter} new messages</h3>    </div>
//     )
//     }
// ReactDOM.render(<NewMessages interval={9000*60}/>,document.getElementById("newMsgs"))
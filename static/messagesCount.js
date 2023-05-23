// function MessageCount(props){
//     const [messages, setMessages] = React.useState([]);

//     const getData = () => {
//         axios.get("/messages").then(response => {
//             setMessages(response.data);
//         })
//     };

//     React.useEffect(() => {
//         getData();
//         setInterval(getData, props.interval);
//     }, []
//     )

//     return (<div>
//             <h4>you have {messages.length} messages</h4>
            
//     </div>
//     )
// }


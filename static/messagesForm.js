function Form() {
    const handleSubmit=(event)=>{
        event.preventDefault();
        console.log(event);
       const newMessage = event.target.elements.myMsg.value;
       axios.post("/addMessage", {message: newMessage}).then(response=>{
        });
    }
    return (
    <form onSubmit={handleSubmit}>
        <input type="text" name="myMsg" style={{"width":"200px"}} />
        <input type="submit" value="Add" />
    </form>
    );
};
ReactDOM.render(<Form/>, document.getElementById("msgForm"));
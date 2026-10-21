import React from 'react'
import Calories from './Calories'
import Chatbot from './Chatbot'

export default function App(){
  return (
    <div style={{padding:20,fontFamily:'Segoe UI, Tahoma, Geneva, sans-serif',background:'#f5f7fa',minHeight:'100vh'}}>
      <h2 style={{textAlign:'center',color:'#667eea'}}>AI Diet Planner</h2>
      <Chatbot />
      <div style={{marginTop:40}}>
        <h3 style={{color:'#764ba2'}}>Calorie Tracker</h3>
        <Calories />
      </div>
    </div>
  )
}

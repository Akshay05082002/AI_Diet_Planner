import React, {useState} from 'react'
import axios from 'axios'

export default function Calories(){
  const [file, setFile] = useState(null)
  const [preds, setPreds] = useState([])
  const [uploadMsg, setUploadMsg] = useState('')

  const handleFile = (e) => setFile(e.target.files[0])

  const upload = async (e) => {
    e.preventDefault()
    if (!file) return setUploadMsg('Choose an image first')

    const data = new FormData()
    data.append('plate_image', file)

    try {
      const res = await axios.post('http://localhost:4000/api/upload', data, { headers: {'Content-Type': 'multipart/form-data'} })
      setPreds(res.data.predictions || [])
      setUploadMsg('Upload successful')
    } catch (err) {
      console.error(err)
      setUploadMsg('Upload failed')
    }
  }

  return (
    <div style={{maxWidth:720}}>
      <form onSubmit={upload}>
        <label style={{display:'block',marginBottom:8}}>Upload meal photo</label>
        <input type="file" accept="image/*" onChange={handleFile} />
        <div style={{marginTop:10}}>
          <button type="submit">Upload to AI API</button>
        </div>
      </form>

      {uploadMsg && <p>{uploadMsg}</p>}

      {preds.length > 0 && (
        <div style={{marginTop:20}}>
          <h4>Detected items</h4>
          <ul>
            {preds.map((p,i) => (
              <li key={i}>{p.name} — {p.calories} kcal</li>
            ))}
          </ul>
          <p style={{fontSize:12,color:'#666'}}>Tip: After detection, use the main app to add items to your daily log.</p>
        </div>
      )}
    </div>
  )
}

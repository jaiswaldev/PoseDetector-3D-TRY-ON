import { useState } from 'react'



function App() {


  return (
    <div class = "flex flex-col items-center justify-center h-screen">
      <h1 class="text-4xl font-bold">Pose Detection</h1>

      <form id="upload-form" enctype="multipart/form-data">
        <input type="file" id="imageInput" name="image" accept="image/*" />
        <button
          type="submit"
          class="button bg-[#4a5568] text-white px-[10px] py-[15px] cursor-pointer"
        >
          Detect Pose
        </button>
      </form>

      <button
        id="startCameraButton"
        class="button bg-[#4a5568] text-white px-[10px] py-[15px] cursor-pointer"
      >
        Start Video
      </button>



      <h3 id="result-heading" class="hidden">Result:</h3>
      <img
        id="outputImage"
        class="fixed hidden h-[400px] w-[400px] left-[35vw]"
      />
    </div>
  )
}

export default App

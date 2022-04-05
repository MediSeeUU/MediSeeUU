import './HomePage.css'
import '../../shared/shared.css'

function HomePage() {
  return (
    // Homepage components, contains article containers (styling in HomePage.css)
    <div className='med_home_content'>
      <article className="med_content__container TopTableHolder">
        <h1>article title</h1>

        <h2>undertitle</h2>

        <p>Example text!</p>
      </article>

      <article className="med_content__container TopTableHolder">
        <h1>article title</h1>

        <h2>undertitle</h2>

        <FillerText />

        <FillerText />
      </article>
    </div>
  )
}

function FillerText() {
  return (
    <p>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean feugiat
      non dui non vehicula. Nunc mattis nisl non luctus convallis. Proin
      bibendum ultricies est non suscipit. Vestibulum vulputate dui elementum,
      tincidunt mauris in, fermentum orci. Duis malesuada sagittis justo, sed
      elementum urna. Aliquam congue nec justo eget tempor. Sed non aliquam ex.
      Integer bibendum lobortis quam non semper. Praesent ac dui vel lectus
      interdum vulputate. Nulla semper hendrerit magna, eu aliquam tellus
      laoreet ac. Integer sed felis vehicula, tincidunt magna id, consequat
      diam. Etiam facilisis tellus dictum metus faucibus scelerisque. Vestibulum
      dolor quam, volutpat facilisis malesuada vitae, porttitor nec quam. Mauris
      laoreet, velit in fermentum luctus, nisl mauris interdum neque, eu
      fermentum sapien ex a felis. Aenean ex erat, volutpat ut rhoncus vitae,
      gravida sit amet risus. Proin sit amet mauris ac urna dignissim imperdiet.
      Maecenas magna ligula, maximus ac gravida malesuada, fringilla non ligula.
      Nunc et mi a ipsum pulvinar faucibus. Ut ac viverra lectus. Aliquam erat
      volutpat. Nullam eget purus sem. Sed aliquam consequat nulla vitae
      fermentum. Donec dignissim nisi vel risus placerat, id bibendum augue
      tristique. Morbi accumsan molestie felis, eget laoreet erat efficitur
      porttitor. Ut vitae risus sed est ultrices interdum. Sed faucibus a felis
      a ornare. Donec eu dapibus eros. Quisque convallis a ante sed sodales. Nam
      a cursus mi, a accumsan est. Integer non purus enim. Mauris sed arcu
      neque. Cras in risus consequat, rutrum metus ut, sollicitudin dolor.
      Suspendisse at libero auctor, efficitur purus eu, bibendum nisi. Etiam ac
      ante velit. Donec accumsan tincidunt mi ac suscipit. Nam a consectetur
      lacus, ut mollis velit. Morbi tempor sapien id nisl sodales ultrices. Orci
      varius natoque penatibus et magnis dis parturient montes, nascetur
      ridiculus mus. Nunc lacinia euismod ipsum ac congue. Fusce lacus lorem,
      iaculis sed dui at, mollis pharetra dui. Nam blandit nibh eu blandit
      eleifend. Fusce at enim laoreet nibh dapibus consequat a ac risus. Etiam
      aliquet, leo a tincidunt fermentum, tellus justo euismod eros, non rutrum
      libero ligula vitae est. Duis at posuere nibh. Aliquam erat volutpat. Sed
      eu felis posuere, imperdiet nibh non, bibendum purus. Maecenas commodo
      efficitur ultrices.
    </p>
  )
}

export default HomePage

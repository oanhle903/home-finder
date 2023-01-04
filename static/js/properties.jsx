'use strict';

function Properties() {
  const [properties, setProperties] = React.useState([]);

  React.useEffect(() => {
    fetch('/properties.json')
      .then((response) => response.json())
      .then((result) => {
        setProperties(result);
      });
  }, []);

  if (properties.length === 0) {
    return <p>Loading...</p>;
  }

  // document.querySelector('#save').addEventListener('click', () => {
  //   document.querySelector('#save').style.display = 'none'; // hide signup button
  // });

  // document.querySelector('#unsave').addEventListener('click', () => {
  //   document.querySelector('#unsave').style.display = 'none'; // hide signup button
  // });

  return (
    <div className='cards_section mx-2'>
      <p className="text-2xl">Properties For Sale</p>

      <hr />

      <div className='cards grid grid-cols-2 gap-2 place-content-stretch'>
        {properties.map((property) => (
          <div className="card " key={property.zpid}>
            <div className="absolute top-2.5 right-2.5 text-3xl">
              <form action={`/properties/${property.zpid}`} method="POST">
                <button type="submit" id="save">
                  <i class="fa-regular fa-heart"></i>
                </button>
              </form>
            </div>
            <div className="absolute top-2.5 right-10 text-3xl">
              <form action={`/properties/${property.zpid}/favorites`} method="POST">
                <button type="submit" id="unsave">
                  <i class="fa-solid fa-heart"></i>
                </button>
              </form>
            </div>
            <div className='card_image'>
              <a href={`/properties/${property.zpid}`}>
                <img src={property.img_src} alt="Home" />
              </a>
            </div>
            <div className='card_info my-2 mx-2'>
              <p className="text-xl font-semibold">${property.price}</p>
              <p>
                <strong>{property.bedrooms}</strong> bds |
                <strong>{property.bathrooms}</strong> ba |
                <strong>{property.lot_area_value }</strong> {property.lot_area_unit}
              </p>
              <p>{property.address}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

}
if (document.querySelector('#all_properties_section')) {

  ReactDOM.render(<Properties />, document.querySelector('#all_properties_section'));
}



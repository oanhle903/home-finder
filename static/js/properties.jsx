'use strict';
// import PropertyCard from "./property_card.jsx";

function Properties() {
  const [properties, setProperties] = React.useState([]);

  React.useEffect(() => {
    fetch('/properties.json') // fetch this route 
      .then((response) => response.json())
      .then((result) => {
        console.log(result);
        setProperties(result);
      });
  }, []);

  if (properties.length === 0) {
    return <p>Loading...</p>;
  }

  return (
    <div className='cards_section mx-2'>
      <p className="text-2xl">Properties For Sale</p>

      <div className='cards grid grid-cols-2 gap-2 place-content-stretch'>
        {properties.map((property) => (
          <PropertyCard property={property} key={property.zpid} />
        ))}
      </div>
    </div>
  );
}

function PropertyCard({ property }) {
  return (
    <div className="card ">
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
    );
}

if (document.querySelector('#all_properties_section')) {

  ReactDOM.render(<Properties />, document.querySelector('#all_properties_section'));
}



'use strict';

// We use a function declaration for initMap because we actually *do* need
// to rely on value-hoisting in this circumstance.
function initMap() {
  const searchedData = document.querySelectorAll('.property-data');

  const firstProperty = searchedData[0].dataset;
  const firstPropertyCoords = {
      lat: +firstProperty.latitude,
      lng: +firstProperty.longitude
  };
  const basicMap = new google.maps.Map(document.querySelector('#map'), {
    center: firstPropertyCoords,
    zoom: 13,
  });
 
  const propertyInfo = new google.maps.InfoWindow();

  for (const div of searchedData) {
    const property = div.dataset;
      // Convert property.price from string to number
  const price = +property.price;

    const propertyInfoContent = `
      <div class="window-content relative flex w-72 h-24 rounded">
        <div class="relative w-1/2 h-full">
          <div class="property-thumbnail absolute h-full w-full ">
            <a href="/properties/${property.zpid}">
              <img
                class="object-cover w-full h-full"
                src="${property.img}"
                alt="houses"
              />
            </a>
          </div>
        </div>

        <div class="property-info pl-4">
          <p class="text-2xl font-semibold my-1">$${price.toLocaleString()}</p>
          <p><strong>${property.bedrooms}</strong> bds |
          <strong>${property.bathrooms}</strong> ba |
          <strong>${property.lot_area_value}</strong> ${property.lot_area_unit}
          </p>
          <p>${property.address}</p>
        </div>

      </div>
    `;

    const propertyMarker = new google.maps.Marker({
      position: {
        lat: +property.latitude,
        lng: +property.longitude,
      },
      map: basicMap, // same as saying map: map
    });

    propertyMarker.addListener('click', () => {
      propertyInfo.close();
      propertyInfo.setContent(propertyInfoContent);
      propertyInfo.open(basicMap, propertyMarker);
    });
  }
}

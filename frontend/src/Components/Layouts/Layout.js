import React from 'react';
import Grid from '@material-ui/core/Grid';
import Header from './Header'
import Navigation from './Navigation/Navigation'
import Footer from './Footer'

export default function CSSGrid() {

  return (
    <div>
        <Header />
        <Grid container>
        <Grid container item xs={2}>
          <Navigation />
        </Grid>        
        <Grid item xs={10} >
           {/* TODO: add overviewMap */}
                    
        </Grid>
      </Grid>
      <Footer />
    </div>
  );
}

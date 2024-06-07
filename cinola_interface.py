
import numpy as np


NUM_SHELLS_FOR_CINOLA = 1


def get_num_neighbors_for_cinola(**kwargs):
    structure = kwargs.get('structure')
    Js_K = kwargs.get('Js_K')

    neigh = get_neigh_from_structure(structure)
    shells_that_matter = get_shells_for_cinola(Js_K)

    num_shells = len(shells_that_matter)

    nums_of_neighbors = [
                            [list(atoms_shells).count(shell) 
                            for shell in set(atoms_shells) 
                            if shell in shells_that_matter
                            ] 
                        for atoms_shells in neigh.shells
                        ]
    nums_of_neighbors = np.array(nums_of_neighbors)


    assert len(set(nums_of_neighbors.flatten())) == 1

    num_neighbors = nums_of_neighbors[0][0]

    assert np.all(nums_of_neighbors == num_neighbors)

    num_neighbors_for_cinola = num_neighbors * num_shells

    return num_neighbors_for_cinola


def get_shells_for_cinola(Js_K):
    shells_that_matter = list(range(1, len(Js_K)+1))
    return shells_that_matter


def get_neighborhoods(structure, Js_K):
        
    # Get neighbor information
    neigh = get_neigh_from_structure(structure)

    shells_that_matter = get_shells_for_cinola(Js_K)

    num_neighbors_for_cinola = get_num_neighbors_for_cinola(structure=structure, Js_K=Js_K)

    neighbors = [
                    [neigh_index if neigh_shell in shells_that_matter else 0 
                    for neigh_index, neigh_shell in zip(atoms_neigh_indices, atoms_shells)
                    ] 
                for atoms_neigh_indices, atoms_shells in zip(neigh.indices+1, neigh.shells)
                ]
    neighbors = np.array(neighbors)


    for atoms_neighbors in neighbors:
        for i_neighbor, neighbor in enumerate(atoms_neighbors):
            if i_neighbor >= num_neighbors_for_cinola:
                assert neighbor == 0

    neighbors = neighbors[:, :num_neighbors_for_cinola]



    Jijs = [
            J * neigh.get_shell_matrix()[iJ].toarray() 
            for iJ, J in enumerate(Js_K)
            ]

    Jijs = [np.expand_dims(Jij, axis=0) for Jij in Jijs]
    Jij = np.concatenate(Jijs, axis=0).sum(axis=0)

    assert set(sorted(np.nonzero(Jij[0])[0])) == set(sorted([neigh_index 
                                                            for array_index, neigh_index 
                                                            in enumerate(neigh.indices[0][:num_neighbors_for_cinola]) 
                                                            if neigh.shells[0][array_index] in shells_that_matter
                                                            ]))

    # FIXME: Jij is just returned for debug. <SB, 2023-07-17>
    return neighbors, Jij


def get_neigh_from_structure(structure):
    neigh = structure.get_neighbors(100)
    return neigh


def get_jij_assign(**kwargs):

    structure = kwargs.get('structure')
    Js_K = kwargs.get('Js_K')


    neigh = get_neigh_from_structure(structure)



    shells_that_matter = list(range(1, len(Js_K)+1))

    num_neighbors_for_cinola = get_num_neighbors_for_cinola(**kwargs)


        
    Jij_assign = [
                    [neigh_shell if neigh_shell in shells_that_matter else 0 
                    for _, neigh_shell in zip(atoms_neigh_indices, atoms_shells)
                    ] 
                for atoms_neigh_indices, atoms_shells in zip(neigh.indices+1, neigh.shells)
                ]
    Jij_assign = np.array(Jij_assign)

    Jij_assign = Jij_assign[:, :num_neighbors_for_cinola]

    return Jij_assign


def get_neighborhoods_string(**kwargs):

    neighbor_file = (
                    f'{NUM_SHELLS_FOR_CINOLA:d}\n{get_num_neighbors_for_cinola(**kwargs):d}\n' + 
                    '\n'.join([' '.join(n.astype(str))
                            for n in get_neighborhoods(**kwargs)[0]
                            ]) +
                    '\n'
                    )
    
    return neighbor_file


def get_jij_assign_string(**kwargs):
        
    Jij_assign_file = (
                    f'{NUM_SHELLS_FOR_CINOLA:d}\n{get_num_neighbors_for_cinola(**kwargs):d}\n' + 
                    '\n'.join([' '.join(n.astype(str)) 
                                for n in get_jij_assign(**kwargs)
                                ]) + 
                    '\n'
                    )
    
    return Jij_assign_file


def get_jvalues_string(Js_K):

    num_Js = len(Js_K)

    Jij_file = f"{num_Js:d}\n" + '\n'.join([f'{J:f}' for J in Js_K]) + '\n'

    return Jij_file


def get_positions_string(structure):
        
    position_file = (
                    f'{len(structure)}\n' + 
                    '\n'.join([' '.join(n.astype(str)) 
                            for n in structure.positions
                            ]) + 
                    '\n'
                    )
    
    return position_file


def get_uniquie_moments(structure):
    unique_moments = list(set(structure.get_initial_magnetic_moments()))
    return unique_moments


def get_anisotropy_and_moment_assign_string(structure):

    unique_moments = get_uniquie_moments(structure)

    moment_idx_per_atom = [unique_moments.index(moment_of_atom) for moment_of_atom in structure.get_initial_magnetic_moments()]

    am_assign_file = (
                    f'{structure.get_number_of_atoms()}\n' + 
                    '\n'.join([' '.join([str(moment_idx_of_atom+1), '1']) 
                            for moment_idx_of_atom in moment_idx_per_atom
                            ]) +
                    '\n'
                    )
    
    return am_assign_file


def get_moments_string(structure):
    unique_moments = get_uniquie_moments(structure)

    moments_file = f'{len(unique_moments)}\n' + '\n'.join([str(float(moment)) for moment in unique_moments]) + '\n'

    return moments_file


def get_aniso_axes_string(structure):

    

    aniso_axes_file = (
                        f'{structure.get_number_of_atoms()}\n' + 
                        '\n'.join(['0.0 0.0 1.0'] * structure.get_number_of_atoms()) + 
                        '\n'
                        )
    
    return aniso_axes_file


def get_aniso_energies_string():
        
    aniso_energies_file = '1\n0.0\n'

    return aniso_energies_file


def get_general_config_string(num_iter_per_temp, H_value, T_low, T_high, T_step):
        
    iterations_per_temperature_cinola = num_iter_per_temp



    H_low = H_value
    H_high = H_value
    H_step = 1.

    config_file = f'''job_name pyiron
    max_spin_change 0.5
    num_steps_in_time {iterations_per_temperature_cinola}
    num_prerelax_steps 1
    T_low {T_low}
    T_high {T_high}
    T_step {T_step}
    H_low {H_low:f}
    H_high {H_high:f}
    H_step {H_step:f}
    H_dir_x 1.0
    H_dir_y 0.0
    H_dir_z 0.0
    '''

    return config_file
